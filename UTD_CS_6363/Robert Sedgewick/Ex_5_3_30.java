/**
 * 
 */
package SubstringSearch;

/*************************

 * @author rohith peddi

 *************************/

/*
 * Two - dimensional search
 * 
 * Rabin Karp algorithm for search patterns in two dimensional text
 * 
 */

public class Ex_5_3_30 {
	
	/** A large number that happens to be prime. */
	public static final long MODULUS = Integer.MAX_VALUE;
	
	/** Radix of the alphabet. Assumes ASCII characters. */
	public static final int RADIX = 256;
	
	/** Powers of RADIX. Used to find the hash when the pattern window is shifted. Analogous to RM in S&W's code. */
	private long[] factors;
	
	/** Height of pattern. */
	private int height;
	
	/** The pattern itself. */
	private char[][] pattern;
	
	/** Hash code of the pattern. */
	private long patternHash;
	
	/** Width of pattern. */
	private int width;
	
	public Ex_5_3_30(char[][] pattern) {
		this.pattern = pattern;
		height = pattern.length;
		width = pattern[0].length;
		factors = new long[(height - 1) + (width - 1) + 1];
		factors[0] = 1;
		for (int i = 1; i < factors.length; i++) {
			factors[i] = (RADIX * factors[i - 1]) % MODULUS;
		}
		patternHash = hash(pattern);
	}
	
	/** Returns true if pattern matches text at position i, j. */
	public boolean check(char[][] text, int i, int j) {
		int x = i;
		int y = j;
		for (int a = 0; a < height; a++) {
			for (int b = 0; b < width; b++) {
				if (text[x][y] != pattern[a][b]) {
					return false;
				}
				y++;
			}
			x++;
			y = j;
		}
		return true;
	}

	/** Returns powers of RADIX, modulo MODULUS, up to (height - 1) * (width - 1). */
	protected long[] getFactors() {
		return factors;
	}
	
	/** Computes (from scratch) and returns the hash of the upper left height * width block of data. */
	protected long hash(char[][] data) {
		long result = 0;
		for (int i = 0; i < height; i++) {
			long rowHash = 0;
			for (int j = 0; j < width; j++) {
				rowHash = (RADIX * rowHash + data[i][j]) % MODULUS;
			}
			result = (RADIX * result + rowHash) % MODULUS;
		}
		return result;
	}
	
	/** Returns an array [i, j], where i and j are the coordinates of a match of pattern in text. */
	public int[] search(char[][] text) {
		long rowStartHash = hash(text);
		long hash = rowStartHash;
		for (int i = 0; i <= text.length - height; i++) {
			if ((hash == patternHash) && check(text, i, 0)) {
				return new int[] {i, 0};
			}
			for (int j = 0; j < text[0].length - width; j++) {
				hash = shiftRight(hash, text, i, j);
				if ((hash == patternHash) && check(text, i, j + 1)) {
					return new int[] {i, j + 1};
				}
			}
			rowStartHash = shiftDown(rowStartHash, text, i);
			hash = rowStartHash;
		}
		return null;
	}
	
	/** Given the hash of the block at i, j, returns the hash of the block at i + 1, j. */
	protected long shiftDown(long hash, char[][] text, int i) {
		for(int p=0; p<width; p++){
			hash = (hash+ MODULUS - (factors[p]*text[i][p] % MODULUS))% MODULUS;
		}
		
		long nexrow =0;
		
		for(int p=0; p<width; p++){
			nexrow = (nexrow*RADIX + text[i+height][p]) % MODULUS;
		}
		
		hash = (hash+nexrow) % MODULUS;
		
		return hash;
	}
	
	/** Given the hash of the block at i, j, returns the hash of the block at i, j + 1. */
	protected long shiftRight(long hash, char[][] text, int i, int j) {
		for(int h=i; h<i+height; h++){
			hash = (hash + MODULUS - (factors[width-h]*text[h][j]% MODULUS))% MODULUS;
		}
		return hash;
	}

}
