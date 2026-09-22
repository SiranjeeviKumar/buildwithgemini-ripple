# app/video_tools.py
"""Video Generation Tool for Ripple - Foresight Angle using gemini-omni-flash-preview."""

import base64
import hashlib
import json
import time
from google import genai
from google.genai import types
from google.cloud import storage
from google.adk.tools import ToolContext

BUCKET_NAME = "ripple-public-assets-qwiklabs-gcp-03-3773bdab8c6e"
PROJECT_ID = "qwiklabs-gcp-03-3773bdab8c6e"


async def generate_decision_item_video(
    item_description: str,
    tool_context: ToolContext = None,
) -> str:
    """Generates a short video for a decision scenario item (e.g. 'SUV navigating Bengaluru traffic' or 'Golden Retriever on 4th floor stairs')
    using Google's Omni model (gemini-omni-flash-preview) in the global region.

    Saves the generated video to Playground artifacts via tool_context.save_artifact,
    uploads the video bytes directly to public GCS storage, and returns the public https URL.

    Args:
        item_description: Description of the item or scenario to generate a video for.
        tool_context: Automatically injected ADK ToolContext for saving artifacts.

    Returns:
        JSON string containing the public Cloud Storage video URL and artifact metadata.
    """
    try:
        # Initialize GenAI Client in global region for gemini-omni-flash-preview
        client = genai.Client(vertexai=True, location="global")

        prompt = f"Continuous realistic video shot of: {item_description}"
        interaction = client.interactions.create(
            model="gemini-omni-flash-preview",
            input=prompt,
        )

        if not hasattr(interaction, "output_video") or not interaction.output_video or not interaction.output_video.data:
            return "Error: No video data returned by gemini-omni-flash-preview."

        raw_data = interaction.output_video.data
        if isinstance(raw_data, str):
            video_bytes = base64.b64decode(raw_data)
        else:
            video_bytes = raw_data

        mime_type = getattr(interaction.output_video, "mime_type", "video/mp4") or "video/mp4"

        # Unique filename
        hash_id = hashlib.md5(f"{item_description}{time.time()}".encode()).hexdigest()[:10]
        filename = f"decision_video_{hash_id}.mp4"

        # 1. Save artifact to ADK Playground Artifacts Panel if tool_context is provided
        if tool_context is not None:
            try:
                artifact_part = types.Part.from_bytes(data=video_bytes, mime_type=mime_type)
                await tool_context.save_artifact(
                    filename=filename,
                    artifact=artifact_part,
                    custom_metadata={"item_description": item_description, "model": "gemini-omni-flash-preview"},
                )
            except Exception as art_err:
                print(f"Notice: artifact saving encountered notice: {art_err}")

        # 2. Upload video bytes directly to public GCS bucket (no local file written)
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        gcs_object_path = f"generated_videos/{filename}"
        blob = bucket.blob(gcs_object_path)
        blob.upload_from_string(video_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{gcs_object_path}"

        result = {
            "item_description": item_description,
            "public_video_url": public_url,
            "artifact_filename": filename,
            "model_used": "gemini-omni-flash-preview",
            "status": "Video generated successfully, saved to Playground artifacts, and uploaded to public GCS.",
        }

        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error generating decision item video: {str(e)}"
