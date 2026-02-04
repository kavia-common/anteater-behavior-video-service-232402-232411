#!/bin/bash
cd /home/kavia/workspace/code-generation/anteater-behavior-video-service-232402-232411/anteater_behavior_video_api
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

