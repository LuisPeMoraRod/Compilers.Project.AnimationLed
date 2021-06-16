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

    public void start(Stage var1) throws Exception {
        Parent var2 = (Parent)FXMLLoader.load(this.getClass().getResource("ide.fxml"));
        var1.setTitle("Animation LED");
        var1.setScene(new Scene(var2, 1200.0D, 700.0D));
        var1.show();
    }

    public static void main(String[] var0) {
        launch(var0);
    }
}
