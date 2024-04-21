package fr.asqel.ultravel.utils;

public class vector {
	public int x;
	public int y;

	public vector(int x, int y) {
		this.x = x;
		this.y = y;
	}

	public vector(vector v) {
		this.x = v.x;
		this.y = v.y;
	}

	public vector add(vector v) {
		return new vector(x + v.x, y + v.y);
	}

	public vector sub(vector v) {
		return new vector(x - v.x, y - v.y);
	}

	public vector negate(vector v) {
		return new vector(-v.x, -v.y);
	}
}
