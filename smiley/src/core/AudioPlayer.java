package core;
import javax.sound.sampled.*;
import java.io.File;
import java.io.IOException;
// this class was generated with the help of uncle GPT
public class AudioPlayer {
    private Clip clip;

    public AudioPlayer(String filePath) {
        try {
            String path ="C:\\Users\\arman\\61bl\\proj3\\proj3\\src\\music\\gg.wav";
            File file = new File(path);
            AudioInputStream audioStream = AudioSystem.getAudioInputStream(file);
            clip = AudioSystem.getClip();
            clip.open(audioStream);
            clip.start();
        } catch (UnsupportedAudioFileException | IOException | LineUnavailableException e) {
            e.printStackTrace();
        }
    }

    public void play() {
        if (clip != null) {
            clip.loop(Clip.LOOP_CONTINUOUSLY);
            clip.start();
        }
    }

    public void stop() {
        if (clip != null) {
            clip.stop();
        }
    }
}
