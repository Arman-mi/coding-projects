package gitlet;

/** Driver class for Gitlet, a subset of the Git version-control system.
 *  @author
 */
public class Main {

    /** Usage: java gitlet.Main ARGS, where ARGS contains
     *  <COMMAND> <OPERAND1> <OPERAND2> ... 
     */
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Please enter a command.");
            return;
        }
        String firstArg = args[0];
        switch (firstArg) {
            case "init": Repository.init();
                break;
            case "add":
                if (args.length < 2) {
                    System.out.println("Please specify a file name.");
                } else {
                    Repository.add(args[1]);
                }
                break;
            case "commit":
                if (args.length < 2) {
                    System.out.println("Please enter a message for your commit");
                } else {
                    Repository.commit(args[1]);
                }
                break;
            case "rm":
                if (args.length < 2) {
                    System.out.println("Please enter  filename for removal");
                } else {
                    Repository.rm(args[1]);
                }
                break;
            case "restore":
                if (args.length == 3 && args[1].equals("--")) {
                    Repository.restore(args[2]);
                } else if (args.length == 4 && args[2].equals("--")) {
                    Repository.restore(args[1], args[3]);
                } else {
                    System.out.println("Invalid arguments for restore command.");
                    break;
                }
            case "log":
                Repository.log();
                break;
            case "global-log":
                Repository.globallog();
                break;
            case "find":
                if (args.length < 2) {
                    System.out.println("Please specify a commit message");
                } else {
                    Repository.find(args[1]);
                }
                break;
            case "status":
                Repository.status();
                break;
            case "branch":
                if (args.length < 2) {
                    System.out.println("Please specify a branch name.");
                } else {
                    Repository.branch(args[1]);
                }
                break;
            case "switch":
                if (args.length < 2) {
                    System.out.println("Please specify a branch name.");
                } else {
                    Repository.switchbranches(args[1]);
                }
                break;
            case "rm-branch":
                if (args.length < 2) {
                    System.out.println("Please specify a branch name.");
                } else {
                    Repository.rmBranch(args[1]);
                }
                break;
            case "reset":
                if (args.length < 2) {
                    System.out.println("Please specify a commit id.");
                } else {
                    Repository.reset(args[1]);
                }
                break;
            default:
                System.out.println("No command with that name exists.");
        }
    }
}
































//            case "merge":
//                if (args.length < 2) {
//                    System.out.println("Please specify a branch name.");
//                } else {
//                    Repository.merge(args[1]);
//                }
//                break;

