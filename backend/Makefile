#################### PACKAGE ACTIONS ###################
reinstall_package:
	@pip uninstall -y chess_board_64 || :
	@pip install -e .

uncompress_model:
	python -c 'from chess_winner.data import save_model,load_compressed_model; save_model(load_compressed_model())'

run_api:
	uvicorn api.fast:app --reload
