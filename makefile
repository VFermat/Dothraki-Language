all: generate_llvm parse_llvm compile_gcc run

generate_llvm:
	@echo "\nAnalysing program"
	python3 main.py ${file}

parse_llvm:
	@echo "\nCompiling program"
	/usr/local/Cellar/llvm/12.0.0_1/bin/llc -filetype=obj ./out/output.ll

compile_gcc:
	gcc ./out/output.o -o ./out/output

run:
	@echo "\nRunning program"
	./out/output

config_env:
	@echo "\nConfig enviroment"
	pip3 install -r requirements.txt
