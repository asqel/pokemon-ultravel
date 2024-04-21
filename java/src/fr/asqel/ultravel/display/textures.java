package fr.asqel.ultravel.display;

import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import javax.imageio.ImageIO;

import fr.asqel.ultravel.utils.file;

public class textures {
	public static BufferedImage MISSING_TEXTURE = file.read_image_jar("/assets/missing_texture.png");
	public static Map<String, Map<String, BufferedImage>> textures = new HashMap<>();

	public static void register() {
		textures.get("obj").put("empty", file.read_image_jar("/assets/empty_texture.png"));
	}

}
