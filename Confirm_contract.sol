pragma solidity ^0.8.19;
contract Enabling_Reliable_Keyword_Search
{

	mapping(string => uint[])public keywordsid;
	mapping(uint => string[])public idkeywords;
	mapping(uint => uint)public idhash;
	string[]public leafs;
	uint[]public history_search;


	function isEqual(string memory a, string memory b) public pure returns (bool)
	{
        bytes memory aa = bytes(a);
        bytes memory bb = bytes(b);
        // 如果长度不等，直接返回
        if (aa.length != bb.length) return false;
        // 按位比较
        for(uint i = 0; i < aa.length; i ++) {
            if(aa[i] != bb[i]) return false;
        }
        return true;
	}
	function Equal(uint a, uint b) public pure returns (bool)
	{
        if(a != b) return false;
		return true;
	}

	function upload(uint id,string memory hash) public
	{
		leafs.push(hash);
		idhash[id] = leafs.length - 1;

	}



	function delete_file(uint id) public
	{	for(uint y=0;y<history_search.length;y++)
		{
			if(Equal(id,history_search[y]))
			{uint len = idkeywords[id].length;
			for (uint i = 0; i < len; i++)
			{
				string memory key;
				key = idkeywords[id][i];
				for (uint j = 0; j < keywordsid[key].length; j++)
				{
					if (Equal(keywordsid[key][j], id))
					{
						if (Equal(j, keywordsid[key].length - 1) || Equal(keywordsid[key].length, 1))
						{
							keywordsid[key].pop();
						}
						else
						{
							for (uint p = j; p < keywordsid[key].length - 1; p++)
							{
								keywordsid[key][p] = keywordsid[key][p + 1];
							}
							keywordsid[key].pop();
						}

					}
				}
			}
			for (uint k = 0; k < len; k++)
			{
				idkeywords[id].pop();
			}}
			}
		uint index = idhash[id];
		if (Equal(1,leafs.length)|| Equal(leafs.length-1,index))
		{
			leafs.pop();
		}
		else
		{
			for(uint o = index; o < leafs.length - 1; o++)
			{
				leafs[o] = leafs[o + 1];
			}
			leafs.pop();
		}


	}

	function construct_search(string memory keyword,uint[] memory id) public
	{

		for(uint i = 0; i < id.length; i ++)
		{
			history_search.push(id[i]);
			keywordsid[keyword].push(id[i]);
			idkeywords[id[i]].push(keyword);
		}
	}

	function search(string memory keyword) public view returns(uint[] memory ids)
	{
		return (keywordsid[keyword]);
	}
	function getleafs()public view returns(string[] memory)
	{
		return leafs;
	}
	function gethashs(uint index)public returns(string memory hash)
	{
		uint id =idhash[index];
		return leafs[id];
	}

}