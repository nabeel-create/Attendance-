# Alternatives & Upgrades

## face_recognition (dlib)
- Much more accurate using face embeddings.
- Installation may require `dlib` which can be hard to build on Streamlit Cloud.
- Suggested: use a VM or Docker where you control the environment, or create a separate branch using `environment.yml` (conda) for deployment.

## Continuous/live detection
- Use `streamlit-webrtc` to capture continuous frames and do real-time recognition instead of single snapshots.

## Security & Privacy
- Always inform and get consent from students before collecting images.
- Store images and DB securely (consider encrypting sensitive storage).
