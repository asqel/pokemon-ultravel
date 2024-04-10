package fr.asqel.ultravel;

import java.awt.*;

public class ultravel extends Frame {
    
    ultravel() {  
        Button b = new Button("Click Me!!");  
        b.setBounds(30,100,80,30);  
        add(b);  
        setSize(300,300);  
        setTitle("This is our basic AWT example");      
        setLayout(null);   
        setVisible(true);  
    }    
    public static void main(String[] args) {
        System.out.println("Hello, World!");
        ultravel w = new ultravel();

    }
}
