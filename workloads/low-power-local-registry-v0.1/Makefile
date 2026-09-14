CC ?= cc
CFLAGS ?= -std=c99 -O2 -Wall -Wextra -Werror

.PHONY: all test clean

all: axm-registry

axm-registry: registry.c
	$(CC) $(CFLAGS) registry.c -o $@

test: axm-registry
	python3 verify.py

clean:
	rm -f axm-registry
