   package mars.venus;
   import mars.*;
   import mars.util.*;
   import java.util.ArrayList;
   import java.awt.*;
   import java.awt.event.*;
   import javax.swing.*;
   import javax.swing.filechooser.FileFilter;
   import java.io.*;
   import java.beans.*;
	
	/*
Copyright (c) 2003-2008,  Pete Sanderson and Kenneth Vollmar

Developed by Pete Sanderson (psanderson@otterbein.edu)
and Kenneth Vollmar (kenvollmar@missouristate.edu)

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files (the 
"Software"), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish, 
distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject 
to the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR 
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

(MIT license, http://www.opensource.org/licenses/mit-license.html)
 */
 
    /**
    * Action  for the File -> Open menu item
    */   			
    public class FileOpenAction extends GuiAction {
    
      private File mostRecentlyOpenedFile;
      private JFileChooser fileChooser;
      private int fileFilterCount;
      private ArrayList fileFilterList;
      private PropertyChangeListener listenForUserAddedFileFilter;
   	 
       public FileOpenAction(String name, Icon icon, String descrip,
                             Integer mnemonic, KeyStroke accel, VenusUI gui) {
         super(name, icon, descrip, mnemonic, accel, gui);
      }
   	 
       /**
   	  * Launch a file chooser for name of file to open
   	  *
   	  * @param e component triggering this call
   	  */
       public void actionPerformed(ActionEvent e) {
         mainUI.editor.open();
      }
   
   }      
