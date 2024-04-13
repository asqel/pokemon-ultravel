package fr.asqel.ultravel.object;

import fr.asqel.ultravel.utils.vector;
import java.awt.image.BufferedImage;
import java.util.Optional;

public class object {
	public vector pos;
	public BufferedImage texture;
	public String id;

	public object(int x, int y, String id, Optional<BufferedImage> texture) {
		this.pos = new vector(x, y);
		if (texture.isPresent())
			this.texture = texture.get();
		else {
			
		}
		this.id = id;
	}
}
