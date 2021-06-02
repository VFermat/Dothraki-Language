all: generate_llvm parse_llvm compile_gcc run

generate_llvm:
	python3 main.py ./examples/test.dt

parse_llvm:
	/usr/local/Cellar/llvm/12.0.0_1/bin/llc -filetype=obj ./out/output.ll

compile_gcc:
	gcc ./out/output.o -o ./out/output

run:
	./out/output

config_env:
	pip3 install -r requirements.txt
