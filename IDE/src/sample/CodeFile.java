package sample;

import java.util.StringTokenizer;

public class CodeFile {

    String fileName;
    String path;

    public CodeFile(String name, String path){
        this.fileName = name;
        this.path = path;
    }

    String getFileName(){
        return this.fileName;
    }

    String getPath(){
        return this.path;
    }
}
