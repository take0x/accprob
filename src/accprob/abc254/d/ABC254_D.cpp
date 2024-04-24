#include <bits/stdc++.h>
using namespace std;

#define V vector
#define rep(i, n) for(int i = 0; i < (int)n; i++)
#define rep_s(i, s, e) for(int i = (int)s; i < (int)e; i++)
#define yon(b) cout << (b ? "Yes" : "No") << endl

template<typename T>
istream &operator>>(istream &is, vector<T> &v) {
	for(T &i : v) is >> i;
	return is;
}

template<typename T>
ostream &operator<<(ostream &os, vector<T> v) {
	for(int i = 0; i < (int)v.size(); i++) os << v.at(i) << (i != v.size() - 1 ? " " : "");
	os << endl;
	return os;
}

template<typename T>
istream &operator>>(istream &is, vector<vector<T>> &v) {
	for(vector<T> &r : v)  for(T &i : r) is >> i;
	return is;
}

template<typename T>
ostream &operator<<(ostream &os, vector<vector<T>> v) {
	for(int i = 0; i < (int)v.size(); i++) {
		for(int j = 0; j < (int)v.at(i).size(); j++) os << v.at(i).at(j) << (j != v.at(i).size() - 1 ? " " : "");
		os << endl;
	}
	return os;
}

int main(void){
}
