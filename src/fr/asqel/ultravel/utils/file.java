package fr.asqel.ultravel.utils;

import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.stream.Collectors;

import javax.imageio.ImageIO;

public class file {

	public static String read_file_jar(String path) {
		InputStream stream = file.class.getResourceAsStream(path);
		if (stream == null)
			return "";
		BufferedReader reader = new BufferedReader(new InputStreamReader(stream));              
		String res = reader.lines().collect(Collectors.joining("\n"));
		return res;
	}

	public static BufferedImage read_image_jar(String path) {
		InputStream stream = file.class.getResourceAsStream(path);
		if (stream == null) {
			System.out.print("ERROR #0 loading image ");
			System.out.println(path);
			System.exit(1);
		}
		try {
			return ImageIO.read(stream);
		}
		catch (Exception e) {
			System.out.print("ERROR #1 loading image ");
			System.out.println(path);
			System.exit(1);
			return null;
		}
	}
	
}
