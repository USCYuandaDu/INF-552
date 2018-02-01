package INF_552;
import java.util.*;

public class TreeNode {

	private String feature_name;
	private HashMap<String, TreeNode> children;
	private int feature_index; // if the TreeNode is the leaf node, then the feature_index == -1
	
	TreeNode(String feature_name, int feature_index) {
		this.feature_name = feature_name;
		this.children = new HashMap<>();
		this.feature_index = feature_index;
	}
	
	public String getFeature_name() {
		return feature_name;
	}

	public void setFeature_name(String feature_name) {
		this.feature_name = feature_name;
	}

	public HashMap<String, TreeNode> getChildren() {
		return children;
	}

	public int getFeature_index() {
		return feature_index;
	}
	
}
