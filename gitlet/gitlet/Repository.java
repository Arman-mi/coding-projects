package gitlet;
import java.text.SimpleDateFormat;


import java.io.File;
import java.util.*;

import static gitlet.Utils.*;



/** Represents a gitlet repository.
 *
 *  does at a high level.
 *
 *  @author
 */
public class Repository {
    /**
     *
     *
     * List all instance variables of the Repository class here with a useful
     * comment above them describing what that variable represents and how that
     * variable is used. We've provided two examples for you.
     */

    /**
     * The current working directory.
     */



    public static final File CWD = new File(System.getProperty("user.dir"));
    /**
     * The .gitlet directory.
     */
    public static final File GITLET_DIR = join(CWD, ".gitlet");


    public static final File STAGING_DIR = Utils.join(GITLET_DIR, "staging");
    public static final File COMMITS_DIR = Utils.join(GITLET_DIR, "commits");
    public static final File BLOBS_DIR = Utils.join(GITLET_DIR, "blobs");
    public static final File HEAD_FILE = Utils.join(GITLET_DIR, "HEAD");
    public static final File STAGING_AREA_FILE = Utils.join(STAGING_DIR, "stagingArea");

    public static final File CURRENT_BRANCH_FILE = Utils.join(GITLET_DIR, "currentBranch");

    public static final File BRANCHES_DIR = Utils.join(GITLET_DIR, "branches");



    //so we make sure that we dont keep making files like a dumb ass
    public static void init() {
        if (GITLET_DIR.exists()) {
            System.out.println("A Gitlet version-control system already exists in the current directory.");
            return;
        }



        GITLET_DIR.mkdir();
        STAGING_DIR.mkdir();
        COMMITS_DIR.mkdir();
        BLOBS_DIR.mkdir();
        BRANCHES_DIR.mkdir();

        Commit initialCommit = new Commit("initial commit", null);

        String initialCommitID = Utils.sha1((Object) Utils.serialize(initialCommit));
        saveCommit(initialCommit);


        //        String commitID = Utils.sha1((Object) Utils.serialize(initialCommit));
        //        File commitFile = Utils.join(CommitsFolder, commitID);
        //        Utils.writeObject(commitFile, firstCommit);
        //
        //        Utils.writeContents(HEAD_FILE, commitID);
        //        saveStagingArea(new HashMap<>());
        File masterBranch = Utils.join(BRANCHES_DIR, "main");
        Utils.writeContents(masterBranch, initialCommitID);
        Utils.writeContents(CURRENT_BRANCH_FILE, "main");
        Utils.writeContents(HEAD_FILE, initialCommitID);
    }


    // now we implement add
    public static void add(String fileName) {
        File file = Utils.join(CWD, fileName);


        if (!file.exists() || file.isDirectory()) {
            System.out.println("File does not exist.");
            return;
        }

        byte[] filecontent = Utils.readContents(file);
        String fileSha1 = Utils.sha1(filecontent);

        String headCommitId = getHeadcommitID();
        Commit headCommit = getCommitbyID(headCommitId);



        HashMap<String, String> stagingArea = loadstagingArea();


        if (fileSha1.equals(headCommit.getFileSha1(fileName))) {
            stagingArea.remove(fileName);

        } else {
            File blobFile = Utils.join(BLOBS_DIR, fileSha1);
            Utils.writeContents(blobFile, (Object) filecontent);

            stagingArea.put(fileName, fileSha1);
        }

        saveStagingArea(stagingArea);
        // Utils.writeObject(Utils.join(StagingDIR, "stagingArea"), stagingArea);


    }

    public static void commit(String message) {
        //OI oI hewui Homelander killed my bloody wife and snatched me bloody son WOMP WOMP
        if (message.trim().isEmpty()) {
            System.out.println("Please enter a commit message.");
            return;
        }
        //HashMap<String, String> stagingArea = Utils.readObject(Utils.join(StagingDIR, "stagingArea"), HashMap.class);

        HashMap<String, String> stagingArea = loadstagingArea();



        if (stagingArea.isEmpty()) {
            System.out.println("No changes added to the commit.");
            return;
        }


        String headCommitId = getHeadcommitID();
        Commit headCommit = getCommitbyID(headCommitId);




        Commit newCommit = new Commit(message, headCommitId);
        assert headCommit != null;
        newCommit.fileSnapshots.putAll(headCommit.fileSnapshots);
        newCommit.fileSnapshots.putAll(stagingArea);

        // GET DOWN MR PRESIDENT SAVE THE FILE

        saveCommit(newCommit);



        saveStagingArea(new HashMap<>());
        String currentBranch = Utils.readContentsAsString(CURRENT_BRANCH_FILE);
        File branchFile = Utils.join(BRANCHES_DIR, currentBranch);
        Utils.writeContents(branchFile, Utils.sha1((Object) Utils.serialize(newCommit)));









    }

    private static void saveCommit(Commit commit) {
        String commitId = Utils.sha1((Object) Utils.serialize(commit));
        File commitFile = Utils.join(COMMITS_DIR, commitId);
        Utils.writeObject(commitFile, commit);
        Utils.writeContents(HEAD_FILE, commitId);
    }





    public static void rm(String filename) {
        HashMap<String, String> stagingArea = loadstagingArea();
        String headCommitId = getHeadcommitID();
        Commit headCommit = getCommitbyID(headCommitId);

        boolean filestaggedforaddition = stagingArea.containsKey(filename);
        boolean fileTrackedInCurrentCommit = headCommit.getFileSha1(filename) != null;


        if (!filestaggedforaddition && !fileTrackedInCurrentCommit) {
            System.out.println("No reason to remove the file.");
            return;
        }
        if (filestaggedforaddition) {
            stagingArea.remove(filename);
        }


        if (fileTrackedInCurrentCommit) {
            stagingArea.put(filename, null); // Indicate that the file should be removed
            File file = Utils.join(CWD, filename);
            if (file.exists()) {
                file.delete();
            }


        }
        saveStagingArea(stagingArea);

    }

    public static void log() {





        String headCommitID = getHeadcommitID();
        Commit currentCommit = getCommitbyID(headCommitID);
        while (currentCommit != null) {
            printCommit(currentCommit);

            String parentCommitId = currentCommit.getParent();
            currentCommit = (parentCommitId == null) ? null : getCommitbyID(parentCommitId);
        }
    }
    public static void printCommit(Commit commit) {
        // for debbuging purposes :

        //        if (commit.getTimestamp() == null) {
        //            System.out.println("Error: Commit timestamp is null for commit ID " +
        //            Utils.sha1(Utils.serialize(commit)));
        //            return;
        //        }



        System.out.println("===");
        System.out.println("commit " + Utils.sha1((Object) Utils.serialize(commit)));
        if (commit.getSecondParent() != null) {
            String parent1 = commit.getParent().substring(0, 7);
            String parent2 = commit.getSecondParent().substring(0, 7);
            System.out.println("Merge: " + parent1 + " " + parent2);
        }

        SimpleDateFormat dateFormat = new SimpleDateFormat("EEE MMM d HH:mm:ss yyyy Z");
        String dateString = dateFormat.format(commit.getTimestamp());
        System.out.println("Date: " + dateString);
        System.out.println(commit.getMessage());
        System.out.println();



    }
    public static void globallog() {
        List<String> commitfiles = Utils.plainFilenamesIn(COMMITS_DIR);
        if (commitfiles != null) {
            for (String commitFile : commitfiles) {
                Commit commit = getCommitbyID(commitFile);

                if (commit != null) {
                    printCommit(commit);
                }
            }
        }
    }

    public static void find(String message) {
        List<String> commitFiles = Utils.plainFilenamesIn(COMMITS_DIR);

        boolean found = false;
        if (commitFiles != null) {
            for (String commitFIle: commitFiles) {
                Commit commit = getCommitbyID(commitFIle);
                if (commit != null && commit.getMessage().equals(message)) {
                    System.out.println(Utils.sha1((Object) Utils.serialize(commit)));
                    found = true;
                }
            }
        }
        if (!found) {
            System.out.println("Found no commit with that message.");
        }
    }
    //    public static final File CURRENT_BRANCH_FILE = Utils.join(GITLET_DIR, "currentBranch");
    //
    //    public static final File BRANCHES_DIR = Utils.join(GITLET_DIR, "branches");




    public static void status() {
        // Branches
        System.out.println("=== Branches ===");
        String currentBranch = Utils.readContentsAsString(CURRENT_BRANCH_FILE);
        List<String> branches = Utils.plainFilenamesIn(BRANCHES_DIR);

        if (branches != null) {
            branches.sort(String::compareTo);
            for (String branch : branches) {
                if (branch.equals(currentBranch)) {
                    System.out.println("*" + branch);
                } else {
                    System.out.println(branch);
                }
            }
        }

        // Staged Files
        System.out.println("\n=== Staged Files ===");
        HashMap<String, String> stagingArea = loadstagingArea();
        TreeSet<String> sortedStagedFiles = new TreeSet<>(stagingArea.keySet());
        for (String file : sortedStagedFiles) {
            if (stagingArea.get(file) != null) {
                System.out.println(file);
            }
        }
        // Removed Files
        System.out.println("\n=== Removed Files ===");
        TreeSet<String> sortedRemovedFiles = new TreeSet<>(stagingArea.keySet());
        for (String file : sortedRemovedFiles) {
            if (stagingArea.get(file) == null) {
                System.out.println(file);
            }
        }

        // Modifications Not Staged For Commit
        System.out.println("\n=== Modifications Not Staged For Commit ===");
        Commit headCommit = getCommitbyID(getHeadcommitID());
        TreeSet<String> modifiedFiles = new TreeSet<>();
        for (String fileName : headCommit.fileSnapshots.keySet()) {
            File file = Utils.join(CWD, fileName);
            if (file.exists()) {
                String fileSha1 = Utils.sha1(Utils.readContents(file));
                if (!fileSha1.equals(headCommit.fileSnapshots.get(fileName)) && !stagingArea.containsKey(fileName)) {
                    modifiedFiles.add(fileName + " (modified)");
                }
            }
            //            else if (!stagingArea.containsKey(fileName)) {
            //                modifiedFiles.add(fileName + " (deleted)");
            //            }
        }
        for (String file : stagingArea.keySet()) {
            File fileInCWD = Utils.join(CWD, file);
            if (!fileInCWD.exists() && stagingArea.get(file) != null) {
                modifiedFiles.add(file + " (deleted)");
            } else if (fileInCWD.exists() && stagingArea.get(file) != null) {
                String fileSha1 = Utils.sha1(Utils.readContents(fileInCWD));
                if (!fileSha1.equals(stagingArea.get(file))) {
                    modifiedFiles.add(file + " (modified)");
                }
            }
        }
        for (String file : modifiedFiles) {
            System.out.println(file);
        }

        // Untracked Files
        System.out.println("\n=== Untracked Files ===");
        TreeSet<String> untrackedFiles = new TreeSet<>();
        for (String fileName : plainFilenamesIn(CWD)) {
            if (!headCommit.fileSnapshots.containsKey(fileName) && !stagingArea.containsKey(fileName)) {
                untrackedFiles.add(fileName);
            }
        }
        for (String file : untrackedFiles) {
            System.out.println(file);
        }

        System.out.println();
    }












    private static void switchBranch(String branchName) {
        File branchFile = Utils.join(BRANCHES_DIR, branchName);
        if (!branchFile.exists()) {
            System.out.println("No such branch exists.");
            return;
        }

        String currentBranch = Utils.readContentsAsString(CURRENT_BRANCH_FILE);
        if (branchName.equals(currentBranch)) {
            System.out.println("No need to switch to the current branch.");
            return;
        }

        String headCommitId = Utils.readContentsAsString(branchFile);
        Commit newHeadCommit = getCommitbyID(headCommitId);
        if (newHeadCommit == null) {
            System.out.println("No commit with that id exists.");
            return;
        }

        // Check for untracked files that would be overwritten
        List<String> cwdFiles = Utils.plainFilenamesIn(CWD);
        Commit currentHeadCommit = getCommitbyID(getHeadcommitID());
        HashMap<String, String> stagingArea = loadstagingArea();
        for (String fileName : cwdFiles) {
            if (!currentHeadCommit.fileSnapshots.containsKey(fileName)
                    && !stagingArea.containsKey(fileName)
                    && newHeadCommit.fileSnapshots.containsKey(fileName)) {
                System.out.println("There is an untracked file in the way; delete it, or add and commit it first.");
                return;
            }
        }

        // Clear the staging area
        saveStagingArea(new HashMap<>());

        // Overwrite files in the working directory with files from the new head commit
        for (String fileName : newHeadCommit.fileSnapshots.keySet()) {
            String fileSha1 = newHeadCommit.fileSnapshots.get(fileName);
            if (fileSha1 != null) {
                File blobFile = Utils.join(BLOBS_DIR, fileSha1);
                if (blobFile.exists()) {
                    byte[] fileContent = Utils.readContents(blobFile);
                    File file = Utils.join(CWD, fileName);
                    Utils.writeContents(file, fileContent);
                }
            }
        }

        // Delete files that are tracked in the current branch but not in the new branch
        for (String fileName : currentHeadCommit.fileSnapshots.keySet()) {
            if (!newHeadCommit.fileSnapshots.containsKey(fileName)) {
                File file = Utils.join(CWD, fileName);
                if (file.exists()) {
                    restrictedDelete(file);
                }
            }
        }

        // Update the current branch
        Utils.writeContents(CURRENT_BRANCH_FILE, branchName);
        Utils.writeContents(HEAD_FILE, headCommitId);
    }









    public static void branch(String branchname) {
        File branchfile = Utils.join(BRANCHES_DIR, branchname);
        if (branchfile.exists()) {
            System.out.println("A branch with that name already exists.");
            return;
        }
        String headCommitID = getHeadcommitID();
        Utils.writeContents(branchfile, headCommitID);


    }


    public static void switchbranches(String branchName) {
        File branchFile = Utils.join(BRANCHES_DIR, branchName);
        if (!branchFile.exists()) {
            System.out.println("No such branch exists.");
            return;
        }

        String currentBranch = Utils.readContentsAsString(CURRENT_BRANCH_FILE);
        if (branchName.equals(currentBranch)) {
            System.out.println("No need to switch to the current branch.");
            return;
        }

        String headCommitId = Utils.readContentsAsString(branchFile);
        Commit newHeadCommit = getCommitbyID(headCommitId);
        if (newHeadCommit == null) {
            System.out.println("No commit with that id exists.");
            return;
        }
        // Check for untracked files that would be overwritten
        List<String> cwdFiles = Utils.plainFilenamesIn(CWD);
        Commit currentHeadCommit = getCommitbyID(getHeadcommitID());
        HashMap<String, String> stagingArea = loadstagingArea();
        for (String fileName : cwdFiles) {
            if (!currentHeadCommit.fileSnapshots.containsKey(fileName)
                &&
                !stagingArea.containsKey(fileName)
                &&
                newHeadCommit.fileSnapshots.containsKey(fileName)) {
                System.out.println("There is an untracked file in the way;"
                        + " delete it, or add and commit it first.");
                return;
            }
        }


        saveStagingArea(new HashMap<>());

        // Overwrite files in the working directory with files from the new head commit
        for (String fileName : newHeadCommit.fileSnapshots.keySet()) {
            String fileSha1 = newHeadCommit.fileSnapshots.get(fileName);
            if (fileSha1 != null) {
                File blobFile = Utils.join(BLOBS_DIR, fileSha1);
                if (blobFile.exists()) {
                    byte[] fileContent = Utils.readContents(blobFile);
                    File file = Utils.join(CWD, fileName);
                    Utils.writeContents(file, fileContent);
                }
            }
        }


        for (String fileName : currentHeadCommit.fileSnapshots.keySet()) {
            if (!newHeadCommit.fileSnapshots.containsKey(fileName)) {
                File file = Utils.join(CWD, fileName);
                if (file.exists()) {
                    file.delete();
                }
            }
        }


        Utils.writeContents(CURRENT_BRANCH_FILE, branchName);
        Utils.writeContents(HEAD_FILE, headCommitId);
    }







    public static void rmBranch(String branchName) {
        File branchFile = Utils.join(BRANCHES_DIR, branchName);
        if (!branchFile.exists()) {
            System.out.println("A branch with that name does not exist.");
            return;
        }

        String currentBranch = Utils.readContentsAsString(CURRENT_BRANCH_FILE);
        if (branchName.equals(currentBranch)) {
            System.out.println("Cannot remove the current branch.");
            return;
        }

        branchFile.delete();
    }














    // im tired and I wanna go home, no no no
    // home as in 20k miles away not the shitty on campus room I have
    // :((((((( josh hug save me
    public static void reset(String commitId) {
        Commit targetCommit = getCommitbyID(commitId);
        if (targetCommit == null) {
            System.out.println();
            return;
        }

        // Check for untracked files that would be overwritten
        List<String> cwdFiles = Utils.plainFilenamesIn(CWD);
        Commit currentHeadCommit = getCommitbyID(getHeadcommitID());
        HashMap<String, String> stagingArea = loadstagingArea();
        for (String fileName : cwdFiles) {
            if (!currentHeadCommit.fileSnapshots.containsKey(fileName)
                    && !stagingArea.containsKey(fileName)
                    && targetCommit.fileSnapshots.containsKey(fileName)) {
                System.out.println("There is an untracked file in the way; delete it, or add and commit it first.");
                return;
            }
        }

        saveStagingArea(new HashMap<>());



        for (String fileName : targetCommit.fileSnapshots.keySet()) {
            File file = Utils.join(CWD, fileName);
            String fileSha1 = targetCommit.fileSnapshots.get(fileName);
            File blobFile = Utils.join(BLOBS_DIR, fileSha1);
            byte[] fileContent = Utils.readContents(blobFile);
            Utils.writeContents(file, fileContent);
        }

        for (String fileName : currentHeadCommit.fileSnapshots.keySet()) {
            if (!targetCommit.fileSnapshots.containsKey(fileName)) {
                File file = Utils.join(CWD, fileName);
                if (file.exists()) {
                    file.delete();
                }
            }
        }

        String currentBranch = Utils.readContentsAsString(CURRENT_BRANCH_FILE);
        File branchFile = Utils.join(BRANCHES_DIR, currentBranch);
        Utils.writeContents(branchFile, commitId);
        Utils.writeContents(HEAD_FILE, commitId);
    }

























    private static HashMap<String, String> loadstagingArea() {
        if (!STAGING_AREA_FILE.exists()) {
            return new HashMap<>();
        }
        return Utils.readObject(STAGING_AREA_FILE, HashMap.class);
    }

    private static void saveStagingArea(HashMap<String, String> stagingArea) {
        Utils.writeObject(STAGING_AREA_FILE, stagingArea);
    }

    private static String getHeadcommitID() {
        return Utils.readContentsAsString(HEAD_FILE);
    }

    private static Commit getCommitbyID(String commitID) {
        File commitFile = Utils.join(COMMITS_DIR, commitID);
        if (!commitFile.exists()) {
            return null;
        }
        return Utils.readObject(commitFile, Commit.class);
    }
    public static void restore(String fileName) {
        restore(getHeadcommitID(), fileName);
    }

    public static void restore(String commitID, String fileName) {
        Commit commit = getCommitbyID(commitID);
        if (commit == null) {
            System.out.println("No commit with that id exists.");
            return;
        }

        String fileSha1 = commit.getFileSha1(fileName);
        if (fileSha1 == null) {
            System.out.println("File does not exist in that commit.");
            return;
        }

        File blobFile = Utils.join(BLOBS_DIR, fileSha1);
        if (!blobFile.exists()) {
            System.out.println("File blob does not exist");
            return;
        }

        byte[] fileContent = Utils.readContents(blobFile);
        File file = Utils.join(CWD, fileName);
        Utils.writeContents(file, fileContent);

        // Remove the file from the staging area if it was staged
        HashMap<String, String> stagingArea = loadstagingArea();
        stagingArea.remove(fileName);
        saveStagingArea(stagingArea);
    }



}









