package fr.asqel.ultravel.utils;

import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.CodeSource;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.util.zip.ZipInputStream;

import javax.imageio.ImageIO;
import javax.print.DocFlavor.URL;

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
	
	public static ArrayList<String> get_files(String _path) {
		if (_path == null)
			return new ArrayList<String>();
		ArrayList<String> files = new ArrayList<String>();
		URI uri;
		try {
			uri = file.class.getResource(_path).toURI();
		}
		catch (Exception e) {
			e.printStackTrace();
			return new ArrayList<String>();
		}
		Path path;
        if (uri.getScheme().equals("jar")) {
			try {
            	FileSystem fileSystem = FileSystems.newFileSystem(uri, Collections.<String, Object>emptyMap());
            	path = fileSystem.getPath(_path);
			}
			catch (Exception e) {
				e.printStackTrace();
				return new ArrayList<String>();
			}
        }
		else {
            path = Paths.get(uri);
        }
        Stream<Path> walk;
		try {
			walk = Files.walk(path, 1);
		}
		catch (IOException e) {
            e.printStackTrace();
            return new ArrayList<String>();
        }
		Iterator<Path> it = walk.iterator();
		ArrayList<String> dirs = new ArrayList<String>();
        while (it.hasNext()) {
			Path current = it.next();
			if (Files.isDirectory(current) && !current.toString().equals(_path))
				dirs.add(current.toString());
			else if (!Files.isDirectory(current))
				files.add(current.toString());
		}
		walk.close();
		try {
			path.getFileSystem().close();
		} 
		catch (Exception e) {}
		
		for (String string : dirs) {
			files.addAll(get_files(string));
		}
		return files;
	}
	
}
