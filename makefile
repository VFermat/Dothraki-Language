all: generate_llvm parse_llvm compile_gcc run

generate_llvm:
	python3 main.py test.dt

parse_llvm:
	/usr/local/Cellar/llvm/12.0.0_1/bin/llc -filetype=obj output.ll

compile_gcc:
	gcc output.o -o output

run:
	./output