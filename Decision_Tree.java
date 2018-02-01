package INF_552;
import java.util.*;
import java.io.*;
import java.util.regex.*;

public class Decision_Tree {

	private int m; // size of datas
	private int n; // size of features
	private ArrayList<String[]> data;
	private String[] features;
	private TreeNode root;
	
	// read file and parse the data
	public void read_and_parse_data(String file_path) {
		File file = new File(file_path);
		Long filelength = file.length(); 
		byte[] filecontent = new byte[filelength.intValue()];
		try {
		    FileInputStream in = new FileInputStream(file);
		    in.read(filecontent);
		    in.close();
		}catch(FileNotFoundException e) {
		    e.printStackTrace();
		}catch(IOException e) {
		    e.printStackTrace();
		}
		
		String content = new String(filecontent);
		Pattern line = Pattern.compile("[0-9]+: (.*);");
		Pattern featureP = Pattern.compile("\\((.*)\\)");
		Matcher fileLine = line.matcher(content);
		Matcher featureM = featureP.matcher(content);
		// Find all matches
		String[] features = {"."};
		if(featureM.find()) {
			features = featureM.group(1).split(", ");
		}
		ArrayList<String[]> lines = new ArrayList<>();
		while(fileLine.find()) {
		  // Get the matching string			
			lines.add(fileLine.group(1).split(", "));
		}
		this.data = lines;
		this.m = data.size();
		this.features = features;
		this.n = features.length;
	}
	// calculate the entropy
	public double entropy(ArrayList<String[]> data) {
		if(data == null || data.size() == 0)
			return 0;
		HashMap<String, Integer> map = new HashMap<>();
		int index = this.n - 1;
		for(String[] line : data) {
			map.put(line[index], map.getOrDefault(line[index], 0) + 1);
		}
		double res = 0.0;
		for(String key : map.keySet()) {
			double P = (double) map.get(key) / data.size();
			res += -P * Math.log(P);
		}
		return res;
	}
	// voting algorithm, only for two candidates
	public String majority(ArrayList<String[]> data) {
		if(data == null || data.size() == 0)
			return null;
		int label_index = this.n - 1;
		String candidate = data.get(0)[label_index];
		int count = 1;
		for(int i = 1; i < data.size(); i++) {
			if(count == 0) {
				candidate = data.get(i)[label_index];
				count = 1;
			} else if(data.get(i)[label_index] == candidate)
				count++;
			else
				count--;
		}
		return candidate;
	}
	// split the data
	public HashMap<String, ArrayList<String[]>> split_data(ArrayList<String[]> data, int feature_index) {
		if(data == null || data.size() == 0)
			return null;
		HashMap<String, ArrayList<String[]>> res = new HashMap<>();
		for(String[] line : data) {
			String key = line[feature_index];
			if(!res.containsKey(key)) 
				res.put(key, new ArrayList<>());
			res.get(key).add(line);
		}
		return res;
	}
	// choose the best feature by Information Gain
	public int choose_the_best_feature(ArrayList<String[]> data, HashSet<Integer> available_features_index) {
		
		double base_entropy = this.entropy(data);
		int base_size = data.size();
		double info_gain = 0;
		int best_index = -1;
		for(int feature_index : available_features_index) {
			HashMap<String, ArrayList<String[]>> res = this.split_data(data, feature_index);
			double cur_entropy = 0.0;
			for(String key : res.keySet()) {
				double p = (double) res.get(key).size() / base_size;
				cur_entropy += p * this.entropy(res.get(key));
			}
			double cur_info_gain = base_entropy - cur_entropy;
			if(cur_info_gain > info_gain) {
				best_index = feature_index;
				info_gain = cur_info_gain;
			}
		}
		return best_index;
	}
	// recursively build the tree
	private TreeNode build_helper(ArrayList<String[]> data, HashSet<Integer> available_features_index) {
		if(data == null || data.size() == 0)
			return null;
		if(available_features_index == null || available_features_index.size() == 0 || this.entropy(data) == 0) {
			// if it is the leaf node, we set the index with -1
			return new TreeNode(this.majority(data), -1);
		} 

		int best_feature_index = this.choose_the_best_feature(data, available_features_index);
		//update the available_features_index
		if(best_feature_index < 0)
			return new TreeNode(this.majority(data), -1);
		available_features_index.remove(best_feature_index);
		TreeNode root = new TreeNode(this.features[best_feature_index], best_feature_index);
		HashMap<String, ArrayList<String[]>> splitted_data = this.split_data(data, best_feature_index);
		for(String key : splitted_data.keySet()) {
			TreeNode child = build_helper(splitted_data.get(key), available_features_index);
			if(child != null)
				root.getChildren().put(key, child);
		}
		return root;
	}
	public void buildTree() {
		HashSet<Integer> set = new HashSet<>();
		for(int i = 0; i < this.n - 1; i++)
			set.add(i);
		this.root = build_helper(this.data, set);
	}
	//print out 
	private void display_helper(TreeNode root, int level) {
		if(root == null)
			return;
		if(root == this.root)
			System.out.print(root.getFeature_name());
		else
			System.out.print(": " + root.getFeature_name());			
		for(String key : root.getChildren().keySet()) {
			System.out.println();
			for(int i = 0; i < level; i++)
				System.out.print(" ");
			System.out.print(key);
			display_helper(root.getChildren().get(key), level + 1);
		}
	}
	//predict
	public String predict(String[] data) {
		TreeNode cur = this.root;
		return predict_helper(cur, data);
	}
	public String predict_helper(TreeNode cur, String[] data) {
		if(cur == null)
			return "can not predict!!!";
		if(cur.getFeature_index() == -1)
			return cur.getFeature_name();
		return predict_helper(cur.getChildren().get(data[cur.getFeature_index()]), data);
	}
	
	public void display() {
		this.display_helper(this.root, 1);
	}
	public ArrayList<String[]> getData() {
		return data;
	}
	public int getM() {
		return m;
	}
	public int getN() {
		return n;
	}
	public String[] getFeatures() {
		return features;
	}
	public TreeNode getRoot() {
		return root;
	}
}
