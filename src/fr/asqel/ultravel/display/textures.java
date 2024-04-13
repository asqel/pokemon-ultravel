package fr.asqel.ultravel.display;

import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.IOException;

import javax.imageio.ImageIO;

import fr.asqel.ultravel.utils.file;

public class textures {
	public static BufferedImage MISSING_TEXTURE = file.read_image_jar("/assets/missing_texture.png");


}
