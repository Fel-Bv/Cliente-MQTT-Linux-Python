#!/usr/bin/env python3
#-*- coding: utf-8 -*-

def e(_):
	_ = _[::-1]
	n = ''

	for l in _:
		n += str(ord(l) ** 2) + ':'

	n = bytes(n[:-1], encoding = 'utf-8', errors = 'strict')

	return n

def d(_):
	if __name__ == e('horse playing football'):
		_ = _.decode(encoding = 'utf-8', errors = 'strict')
		n = ''

		for l in _.split(':'):
			try: n += chr(int(int(l) ** .5))
			except ValueError as exc: print(exc)

		return bytes(n[::-1], encoding = 'utf-8', errors = 'strict')