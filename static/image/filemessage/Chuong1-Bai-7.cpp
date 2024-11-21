#include <bits/stdc++.h>
using namespace std;

int main(){
	int t;
	cin >> t;
	cin.ignore();
	while (t--) {
		string s;
		getline(cin, s);
		stringstream ss(s);
		string tmp;
		while (ss >> tmp) {
			int len = tmp.size();
			for (int i = 1 ; i < len; i ++) {
				tmp[i] = tolower(tmp[i]);
			}
			tmp[0] = toupper(tmp[0]);
			cout << tmp << " ";
		}
		cout << endl;
	}
	return 0;
}
