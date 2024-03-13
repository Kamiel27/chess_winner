#################### PACKAGE ACTIONS ###################
reinstall_package:
	@pip uninstall -y chess_board_64 || :
	@pip install -e .

uncompress_model:
	python -c 'from chess_winner.data import save_model,load_compressed_model; save_model(load_compressed_model())'

run_api:
	uvicorn api.fast:app --reload

docker_build :
	docker build -t  ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GCP_REPO_NAME}/${GAR_IMAGE}:prod .

docker_push :
	docker push ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GCP_REPO_NAME}/${GAR_IMAGE}:prod

gcloud_run :
	gcloud run deploy --image ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GCP_REPO_NAME}/${GAR_IMAGE}:prod --memory ${GAR_MEMORY} --region ${GCP_REGION} --env-vars-file .env.yaml
