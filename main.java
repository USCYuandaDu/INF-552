package INF_552;
import java.net.URL;
import java.util.*;
public class main {

	public static void main(String[] args) {

		Decision_Tree tree = new Decision_Tree();
		URL base = tree.getClass().getResource("");
		String filename = base.getFile() + "dt-data.txt";
		tree.read_and_parse_data(filename); // read data from file
		tree.buildTree(); // build the decision tree
		tree.display(); // print the tree 
		//predict the given data
		String result = tree.predict(new String[] {"Moderate", "Cheap", "Loud", "City-Center", "No", "No"});
		System.out.println();
		System.out.println("predict result:" + result);
	}
}
