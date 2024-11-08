package gitlet;

import java.util.Date;
import java.io.Serializable;
import java.util.HashMap;




public class Commit implements Serializable {


    /**
     *
     *
     * List all instance variables of the Commit class here with a useful
     * comment above them describing what that variable represents and how that
     * variable is used. We've provided one example for `message`.
     */

    /**
     * The message of this Commit.
     */

    private Date time;
    private String parent;
    private String message;
    HashMap<String, String> fileSnapshots;
    String secondParent;
    Date timestamp;



    public Commit(String message, String parent) {
        this.message = message;
        this.parent = parent;
        this.timestamp = new Date();
        this.fileSnapshots = new HashMap<>();
    }

    public String getFileSha1(String filename) {
        return fileSnapshots.get(filename);
    }

    public String getMessage() {
        return message;
    }


    public Date getTimestamp() {
        if (timestamp == null) {
            timestamp = new Date();
        }
        return timestamp;
    }

    public String getParent() {
        return parent;
    }

    public String getSecondParent() {
        return secondParent;
    }

    public void setSecondParent(String secondParent) {
        this.secondParent = secondParent;
    }
    public void addFileSnapshot(String fileName, String fileSha1) {
        fileSnapshots.put(fileName, fileSha1);
    }
}
