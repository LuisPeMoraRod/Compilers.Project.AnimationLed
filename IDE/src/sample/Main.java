//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//

package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class Main extends Application {
    public Main() {
    }

    public void start(Stage stage) throws Exception {
        Parent window = (Parent)FXMLLoader.load(this.getClass().getResource("ide.fxml"));
        stage.setTitle("Animation LED");
        stage.setScene(new Scene(window, 1000, 700));
        stage.setResizable(false);
        stage.show();
    }

    public static void main(String[] var0) {
        launch(var0);
    }
}
