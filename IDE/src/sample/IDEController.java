package sample;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.ListView;
import javafx.scene.control.ScrollBar;
import javafx.scene.control.TextArea;
import javafx.scene.input.InputMethodEvent;
import javafx.stage.FileChooser;
import sun.font.TrueTypeGlyphMapper;

import java.io.*;
import java.util.List;
import java.util.Scanner;

public class IDEController {

    File file;
    final String aledFile = "/Users/moniwaterhouse/Projects/Compilers.Project.AnimationLed/IDE/code.aled";
    final String command = "python3 ";
    final String mainFile = "/Users/moniwaterhouse/Projects/Compilers.Project.AnimationLed/Compiler/main.py ";
    int errorLine;

    @FXML
    Button btnOpenFile;

    @FXML
    TextArea textCode;

    @FXML
    TextArea textOutput;

    @FXML
    ListView listFiles;



    public void openFile(ActionEvent actionEvent) {

        try{
            FileChooser fileChooser = new FileChooser();
            fileChooser.setTitle("Open Resource File");
            file = fileChooser.showOpenDialog(btnOpenFile.getScene().getWindow());

            if (file!=null){
                textCode.clear();
                textOutput.clear();
                Scanner s = new Scanner(new File(file.getAbsolutePath())).useDelimiter("\\n");

                while (s.hasNext()) {

                    textCode.appendText(s.next() + "\n"); // else read the next token

                }
            }

        }

        catch (IOException e){
            System.err.println(e);
        }


    }

    public void compile(ActionEvent actionEvent) throws IOException {

        compileFile();

    }

    public void runCode(ActionEvent actionEvent) {
        compileFile();

        if (errorLine > 0){
            textOutput.appendText("Error: Unable to execute program");
        }
        else{
            textOutput.appendText("Executing code...");
            executeFile();
        }

    }


    public void countLines(){
        System.out.println(textCode.getText().split("\n").length);
    }


    public void compileFile(){
        try {

            String code = textCode.getText();
            BufferedWriter writer = new BufferedWriter(new FileWriter(aledFile));
            writer.write(code);

            writer.close();

        } catch (IOException ex) {
            System.out.println(ex.getMessage());
        }

        try{
            textOutput.clear();
            Runtime rt = Runtime.getRuntime();
            Process pr = rt.exec(command + mainFile + aledFile);
            pr.getOutputStream();
            BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));
            String line;
            while ((line = in.readLine()) != null) {
                if (isNumeric(line)){
                    errorLine = Integer.parseInt(line);
                }
                else{
                    errorLine = 0;
                    textOutput.appendText(line +"\n");
                }

            }
        }
        catch (IOException e){
            System.err.println(e);
        }
    }

    public void executeFile(){
        try{

            Runtime rt = Runtime.getRuntime();
            Process pr = rt.exec(command + mainFile + aledFile);
            pr.getOutputStream();

        }
        catch (IOException e){
            System.err.println(e);
        }
    }

    public boolean isNumeric(String string){
        try{
            errorLine = Integer.parseInt(string);
            return true;
        }
        catch (NumberFormatException e){
            return false;
        }
    }
}

