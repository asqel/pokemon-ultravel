package fr.asqel.ultravel;


import fr.asqel.ultravel.display.screen;
import fr.asqel.ultravel.display.textures;
import fr.asqel.ultravel.utils.file;

public class ultravel {
	public static String src_folder;
	public screen SCREEN;

	private void setup() {
		SCREEN = new screen();
	}

	ultravel() {
	}
	public static void main(String[] args) {
		System.out.println("Hello, World!");
		ultravel game = new ultravel();
		game.setup();
		game.SCREEN.blit(100, 100, textures.MISSING_TEXTURE);
	}
}
