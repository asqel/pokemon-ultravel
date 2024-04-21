package fr.asqel.ultravel.object.contents;

import java.awt.image.BufferedImage;
import java.util.Optional;

import fr.asqel.ultravel.display.textures;
import fr.asqel.ultravel.object.object;

public class air extends object{

	public air(int x, int y) {
		super(x, y, "air", textures.MISSING_TEXTURE);
	}
	
}
