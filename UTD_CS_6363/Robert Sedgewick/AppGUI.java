import java.awt.Container;
import java.awt.GridLayout;
import java.awt.Rectangle;
import java.awt.event.*;

import javax.swing.*;

import edu.princeton.cs.algs4.StdOut;

public class AppGUI extends JFrame {
	
	private JButton filmSearchButton;
	private JButton actorSearchButton;
	private JLabel filmLabel;
	private JLabel actorLabel;
	private JTextField filmField;
	private JTextField actorField;
	
	private JLabel resultLabel;
	private JTextArea resultArea;
	private JScrollPane resultScrollPane;
	
	private JPanel filmPanel;
	private JPanel actorPanel;
	private JPanel resultPanel;
	
	
	/************* INITIALIZER ***************/
	
	public void initialize(){
		
		filmSearchButton = new JButton("SEARCH");
		actorSearchButton = new JButton("SEARCH");
		
		filmLabel = new JLabel("FILM NAME:");
		actorLabel = new JLabel("ACTOR NAME:");
		
		filmField = new JTextField(20);
		actorField = new JTextField(20);
		
		resultLabel = new JLabel("RESULT:");
		resultArea = new JTextArea(10,35);
		resultArea.setLineWrap(true);
		resultArea.setWrapStyleWord(true);
		resultScrollPane = new JScrollPane(resultArea);
		resultScrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
		
		
		filmPanel  = new JPanel();
		actorPanel = new JPanel();
		resultPanel = new JPanel();
		
	}
	
	/************* ADDING LISTENERS ***************/
	
	public void addListeners(){
		
		Database ob = new Database();
		
		filmSearchButton.addActionListener(new ActionListener(){

			@Override
			public void actionPerformed(ActionEvent e) {
				String search_film = filmField.getText();
				String result = ob.film.get(search_film).toString();
				resultArea.setText(result);
			}
			
		});
		
		actorSearchButton.addActionListener(new ActionListener(){

			@Override
			public void actionPerformed(ActionEvent e) {
				String search_actor = actorField.getText();
				String result = ob.actor.get(search_actor).toString();
				resultArea.setText(result);
			}
			
		});
	}
	
	/************* SETTING UP PANELS ***************/
	
	public void setPanels(){
		
		filmPanel.add(filmLabel); filmPanel.add(filmField); filmPanel.add(filmSearchButton);
		actorPanel.add(actorLabel); actorPanel.add(actorField); actorPanel.add(actorSearchButton);
		resultPanel.add(resultLabel);resultPanel.add(resultScrollPane);
		
		Container contentPane = getContentPane();
		contentPane.setLayout(new GridLayout(3,1));
		contentPane.add(filmPanel); contentPane.add(actorPanel); 
		contentPane.add(resultPanel);
		
	}
	
	/************* CONSTRUCTOR ***************/
	
	public AppGUI(){
		
		setTitle("INTERNET MOVIE DATABASE");
		setSize(500,600);
		setLocation(200,200);
		
		//Window Listeners
		addWindowListener(new WindowAdapter(){
			public void windowClosing(WindowEvent e){
				System.exit(0);
			} //windowClosing
		});
		
		initialize();
		addListeners();
		setPanels();		
		
		//setResizable(false);
	}
	
	/************* GETTER & SETTER ***************/
	
	
	
	/************* MAIN ***************/
	
	public static void main(String args[]){
		JFrame f = new AppGUI(); f.show();
	}


}
