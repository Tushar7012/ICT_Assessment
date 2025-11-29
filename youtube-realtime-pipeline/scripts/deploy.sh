echo "=========================================="
echo "YouTube Real-Time Pipeline Deployment"
echo "=========================================="

if ! command -v gcloud &> /dev/null
then
    echo "gcloud CLI not found. Please install Google Cloud SDK."
    exit 1
fi

# Deploy Webhook Service
echo ""
echo "Deploying Webhook Service..."
gcloud functions deploy youtube-webhook \
  --runtime python311 \
  --trigger-http \
  --entry-point app \
  --source ./webhook_service \
  --allow-unauthenticated \
  --set-env-vars YOUTUBE_API_KEY=$YOUTUBE_API_KEY,MONGODB_URL=$MONGODB_URL

# Deploy API Service
echo ""
echo "Deploying API Service..."
gcloud functions deploy youtube-api \
  --runtime python311 \
  --trigger-http \
  --entry-point app \
  --source ./api \
  --set-env-vars API_KEY=$API_KEY,MONGODB_URL=$MONGODB_URL

echo ""
echo "Deployment Complete!"
echo "=========================================="
