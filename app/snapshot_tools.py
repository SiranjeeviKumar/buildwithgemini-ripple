# app/snapshot_tools.py
"""Visual Reality Snapshot Generator Tool for Ripple - Foresight Angle."""

import hashlib
import json
import time
from io import BytesIO
from google.cloud import storage
from PIL import Image, ImageDraw, ImageFont

BUCKET_NAME = "ripple-public-assets-qwiklabs-gcp-03-3773bdab8c6e"
PROJECT_ID = "qwiklabs-gcp-03-3773bdab8c6e"


def generate_reality_snapshot(
    scenario_title: str,
    ideal_vs_reality_contrast: str,
    key_friction_summary: str,
) -> str:
    """Generates a visual reality snapshot card for a decision scenario and uploads it to public Cloud Storage.

    Args:
        scenario_title: Short title of the decision (e.g., 'Adopting a 75lb Dog in a 4th-Floor Walkup').
        ideal_vs_reality_contrast: High-level contrast description (e.g., 'Ideal: Cozy puppy cuddles on couch vs. Reality: Carrying 75lb dog down 76 rain-slicked stairs at 2 AM').
        key_friction_summary: Key operational friction summary (e.g., '3,640 annual stair trips | $17.8k 5-year TCO | 780 hrs/yr diverted').

    Returns:
        JSON string containing the public HTTPS image URL of the generated reality snapshot card.
    """
    try:
        # Create a 800x450 dark-mode snapshot graphic card
        width, height = 800, 450
        img = Image.new("RGB", (width, height), color="#111827")
        draw = ImageDraw.Draw(img)

        # Draw border frame
        draw.rectangle([15, 15, width - 15, height - 15], outline="#3B82F6", width=3)
        draw.rectangle([25, 25, width - 25, 80], fill="#1F2937", outline="#4B5563", width=1)

        # Header Title
        draw.text((40, 38), "RIPPLE REALITY SNAPSHOT", fill="#60A5FA")
        draw.text((40, 56), scenario_title[:60], fill="#F9FAFB")

        # Visual Divider
        draw.line([(40, 95), (width - 40, 95)], fill="#374151", width=2)

        # Ideal vs Reality Section
        draw.rectangle([40, 115, 760, 290], fill="#1F2937", outline="#374151", width=1)
        draw.text((60, 130), "⚡ IDEAL VS. REALITY CONTRAST", fill="#F59E0B")

        # Wrap text manually
        contrast_lines = [
            ideal_vs_reality_contrast[i : i + 75]
            for i in range(0, len(ideal_vs_reality_contrast), 75)
        ][:4]
        y_pos = 160
        for line in contrast_lines:
            draw.text((60, y_pos), line, fill="#E5E7EB")
            y_pos += 24

        # Key Friction Banner
        draw.rectangle([40, 310, 760, 400], fill="#311B92", outline="#7C3AED", width=2)
        draw.text((60, 325), "📊 COMPOUNDING FRICTION SUMMARY", fill="#A78BFA")

        friction_lines = [
            key_friction_summary[i : i + 75]
            for i in range(0, len(key_friction_summary), 75)
        ][:2]
        y_pos = 350
        for line in friction_lines:
            draw.text((60, y_pos), line, fill="#F3E8FF")
            y_pos += 22

        # Convert image to PNG bytes
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()

        # Generate unique filename hash
        hash_id = hashlib.md5(f"{scenario_title}{time.time()}".encode()).hexdigest()[:10]
        filename = f"snapshots/snapshot_{hash_id}.png"

        # Upload to public GCS bucket
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(image_bytes, content_type="image/png")

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

        result = {
            "scenario_title": scenario_title,
            "public_snapshot_image_url": public_url,
            "status": "Reality snapshot generated and uploaded successfully to public Cloud Storage.",
        }

        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error generating reality snapshot: {str(e)}"
