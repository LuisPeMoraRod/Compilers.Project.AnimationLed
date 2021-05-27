# TokenType is our enum for all the types of tokens.
import enum

class TokenType(enum.Enum):
	EOF = -1
	SEMICOLON = 0
	NUMBER = 1
	IDENT = 2
	STRING = 3
	DOT = 4
	COMA = 5
	# Keywords.
	For = 101
	In = 102
	If = 103
	Procedure = 104
	true = 105
	false = 106
	# Operators.
	EQ = 201  
	PLUS = 202
	MINUS = 203
	ASTERISK = 204
	SLASH = 205
	EQEQ = 206
	NOTEQ = 207
	LT = 208
	LTEQ = 209
	GT = 210
	GTEQ = 211
	SLASHD = 212
	MODULE = 213
	# Other symbols
	CURLYBRACKETLEFT = 301
	CURLYBRACKETRIGHT = 302
	ROUNDBRACKETLEFT = 303
	ROUNDBRACKETRIGHT = 304
	SQRBRACKETLEFT = 305
	SQRBRACKETRIGHT = 306