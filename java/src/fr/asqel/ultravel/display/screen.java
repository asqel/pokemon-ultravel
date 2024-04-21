package fr.asqel.ultravel.display;

import java.awt.Frame;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.awt.image.ImageObserver;
import java.util.function.Supplier;

public class screen extends Frame{
	public BufferedImage back_screen;
	public Graphics2D back_screen_graphics;
	
	public screen() {
		setSize(500, 500);
		setVisible(true);
		setIgnoreRepaint(true);
		back_screen = new BufferedImage(500, 500, BufferedImage.TYPE_INT_ARGB);
		back_screen_graphics = back_screen.createGraphics();
	}
	public void blit(int x, int y, BufferedImage img) {
		back_screen_graphics.drawImage(img, x, y, null);
	}

	public void update() {
		repaint();
	}

	@Override
	public void paint(Graphics g) {
        super.paint(g);
        g.drawImage(back_screen, 0, 0, this);
    }
	
}
