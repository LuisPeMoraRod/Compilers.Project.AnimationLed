package sample;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.ListView;
import javafx.scene.control.ScrollBar;
import javafx.scene.control.TextArea;
import javafx.scene.input.InputMethodEvent;
import javafx.stage.FileChooser;

import java.io.*;
import java.util.List;
import java.util.Scanner;

public class IDEController {

    List<CodeFile> openFiles;

    @FXML
    Button btnOpenFile;

    @FXML
    TextArea textCode;

    @FXML
    TextArea textOutput;

    @FXML
    ListView listFiles;

    File file;

    public void openFile(ActionEvent actionEvent) {

        try{
            FileChooser fileChooser = new FileChooser();
            fileChooser.setTitle("Open Resource File");
            file = fileChooser.showOpenDialog(btnOpenFile.getScene().getWindow());

            if (file!=null){
                Scanner s = new Scanner(new File(file.getAbsolutePath())).useDelimiter("\n");
                while (s.hasNext()) {

                    textCode.appendText(s.next() + " "); // else read the next token

                }
            }

        }

        catch (IOException e){
            System.err.println(e);
        }


    }

    public void compile(ActionEvent actionEvent) throws IOException {
        try{
            Runtime rt = Runtime.getRuntime();
            Process pr = rt.exec("python3 " + "/Users/moniwaterhouse/Projects/Compilers.Project.AnimationLed/IDE/src/sample/test2.py");
            pr.getOutputStream();
            BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));
            String line;
            while ((line = in.readLine()) != null) {
                textOutput.appendText(line +"\n");

            }
        }
        catch (IOException e){
            System.err.println(e);
        }

    }

    public void runCode(ActionEvent actionEvent) {
        System.out.println(textCode.getText().split("\n").length);
    }

    public void saveFile(ActionEvent actionEvent) {
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter(file.getAbsolutePath()));
            writer.write("Hola");

            writer.close();
        } catch (IOException ex) {
            System.out.println(ex.getMessage());
        }

    }

    public void newFile(ActionEvent actionEvent) {

        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Open Resource File");
        file = fileChooser.showSaveDialog(btnOpenFile.getScene().getWindow());
        String code = textCode.getText();

        if (file != null) {
            CodeFile codeFile = new CodeFile(file.getName(), file.getAbsolutePath());
            openFiles.add(codeFile);

        }
    }

}

