(
var instruments=[\bdrum, \sdrum, \clap,\hhclosed,\hhopen,\hitom,\lotom];
var sliders;
var pop;
var size=32;
var clusters=9;
var tempCopy;
var tempOneCopy;
var buttons;
// var seqs={{0}!size}!9;
var sequences={{{0}!size}!clusters}!instruments.size;
// var prstPth = PathName("/Volumes/Coochie/SOUND/presets/anushri/glacial");
var folder = PathName(PathName(thisProcess.nowExecutingPath).pathOnly);
var reaperFolder = PathName("/Users/SomeRandomer/Library/Application Support/REAPER/Data/drum_styles/").pathOnly.postln;
var presetNames= folder.folders;
var itemsFolder = presetNames.collect{|i| i.folderName};
var currentCluster=0;
var currentPreset=0;
var setOneSeq={|inst, clust, value|
	sequences[inst][clust]=(value*255).round.asInteger;
};

var clearAll={
	sequences={{{0}!size}!clusters}!instruments.size;
};

var getSeqs={|clust|
	sliders.do{|i,in|
		i.value = sequences[in][clust].postln/255;
	}
};

var copy={|cluster|

	tempCopy = sequences.collect{|i| i[currentCluster];};
	tempCopy.postln;

};
var paste={|cluster|
	instruments.do{|i,in|
		sequences[in][currentCluster]=tempCopy[in];

	};
	// tempCopy = sequences.collect{|i| i[currentCluster];};
	tempCopy.postln;

};
var pasteOne={|inst,cluster,item,value|

	sequences[inst][currentCluster][item]=value;

};

var load={|preset|
	var fileToLoad=(presetNames[preset].fullPath++presetNames[preset].folderName++".preset").postln;
	sequences = Object.readArchive(fileToLoad);
	sequences.postln;
	getSeqs.value(currentCluster);

};
var save={
	var path= presetNames[currentPreset].fullPath;
	var bool = itemsFolder.detect({|i| i==t.string}).notNil;
	var newPath;
	var newString="";
	// var kicks="",snares="",claps="",hatc="",hato="",hito="",loto="";
	// setSeqs.value(0);
	if(bool.postln==false,{File.mkdir(folder.fullPath++"/"++t.string);});
	sequences.writeArchive((folder.fullPath++"/"++t.string++"/"++t.string++".h").standardizePath);
	f = File.new((folder.fullPath++"/"++t.string++"/"++t.string++".h").standardizePath, "w");
	// f = File.new((folder.fullPath++"/"++t.string++"/"++t.string++".txt").standardizePath, "w");


	instruments.do{|ins, ii|
		clusters.do{|cl,icl|
			newString=newString++  "{"++sequences[ii][cl].asCompileString.drop(1).drop(-1).select{|i| i!=$\ }++" }, ";

		};
		if(ii<(instruments.size-1),{newString=newString.drop(-1)});

	};
	newString="Style "++t.string++" = { "++"\""++t.string.toUpper++"\""++" , {"++newString;
	newString=newString.drop(-2)++" } };";
	newString.postln;
	/*clusters.do{|cluster,in|

	cluster.postln;
	instruments.do{|i, in|
	var temp=i++"|"++sequences[in][cluster].asCompileString.drop(1).drop(-1).select{|i| i!=$\ }+"\t";
	newString=newString+temp;

	};*/
	// kicks=kicks++"kick|"++sequences[0][cluster].asCompileString.drop(1).drop(-1).select{|i| i!=$\ }+"\t";
	// snare=snare++"snare|"++sequences[1][cluster].asCompileString.drop(1).drop(-1).select{|i| i!=$\ }+"\t";
	// claps=claps++"claps|"++sequences[2][cluster].asCompileString.drop(1).drop(-1).select{|i| i!=$\ }+"\t";
	// snares=snares++"snare"++sequences[1][cluster].asCompileString;
	// snares=snares++"snare"++sequences[cluster][1].asCompileString;
	// snares=i.asCompileString;




	// };
	// newString=sequences.asCompileString.replace(", ",",").replace;
	// sequences.asString.postln;
	// newString=kicks++snares;
	// f.putString(sequences.asCompileString);
	f.putString(newString);
	f.close;
	refresh.value();

};
var refresh={
	presetNames= folder.folders;
	itemsFolder = presetNames.collect{|i| i.folderName};
	pop.items=(itemsFolder);
	pop.value(1);
};

// var ser;
w = Window("ORSINI DRUMMER FUCKER", 900@850, resizable: true, scroll: true).front;
w.view.decorator = FlowLayout(w.view.bounds);
t=TextField(w,550@20).string_(presetNames[currentPreset].folderName);
Button(w, 50@20).states_([["save", Color.white, Color.black]])
.action_({ |button|
	"save".postln;
	save.value();
	// setSeqs.value(currentCluster);
	// seqs.postln;


});
pop=PopUpMenu(w, 120@20).items_(itemsFolder).action_{|menu|

	t.string_(menu.item);
	load.value(menu.value);

};
Button(w, 50@20).states_([["copy", Color.white, Color.black]])
.action_({ |button|
	"save".postln;
	copy.value();
	// setSeqs.value(currentCluster);
	// seqs.postln;


});
Button(w, 50@20).states_([["paste", Color.white, Color.black]])
.action_({ |button|
	"save".postln;
	paste.value();
	getSeqs.value(currentCluster);
	// seqs.postln;


});
Button(w, 20@20).states_([["x", Color.white, Color.red]])
.action_({ |button|
	"clear".postln;
	clearAll.value();
	getSeqs.value(currentCluster);
	// seqs.postln;


});


buttons=9.collect{|cluster, in|
	c=Button(w, 60@20).states_([["cluster "++cluster, Color.white, Color.black],["cluster "++cluster, Color.white, Color.red]])
	.action_({ |button|
		getSeqs.value(cluster);
		currentCluster=cluster.postln;
		buttons.do{|i, in|
			if(in==currentCluster,{i.value=1},{i.value=0});

		};

		// h = Object.readArchive(prstPth.fullPath);
		// c =	(cluster * 3).postln;
		/*m.bdrum.value=h[c+0]/255;
		m.sdrum.value=h[c+1]/255;
		m.hhats.value=h[c+2]/255;*/
	});

};

// getSeqs.value(currentCluster);

sliders=instruments.collect{|i, in|
	var mt = MultiSliderView(w, Rect(0, 0, 890, 70));
	mt.step=0.333;
	mt.value_(Array.fill(size, {0.0}));
	mt.isFilled_(true); // width in pixels of each stick
	mt.indexThumbSize_((900-(32*4)/33)); // spacing on the value axis
	mt.gap_(4);

	mt.action_({|multi|
		setOneSeq.value(in, currentCluster, multi.value.postln);

	});
	32.do{| i |
		if(i%4==0,
			{StaticText(w, (890/38)@10).string_(i+1).align_(\center)},
			{StaticText(w, (890/38)@10).string_(i+1).align_(\center).stringColor_(Color.gray)}
		)

	};
	f=Button(w, 300@20).states_([[i, Color.white, Color.black]])
	.action_({ |button|
		// seqs[currentCluster]=(m[i].value*255).round;
		// a[i].postln.string_((m[i].value*255).round.asString.postln);
	});
	/*Slider(w, 100@20).action_({ |slider|
		sequences[in][currentCluster]=sequences[in][currentCluster]+([-10.0,10.0].asSpec.map(slider.value));
		getSeqs.value(currentCluster)
		// pasteOne.value(in);
		// seqs[currentCluster]=(m[i].value*255).round;
		// a[i].postln.string_((m[i].value*255).round.asString.postln);
	});*/
	Button(w, 50@20).states_([["copy", Color.white, Color.black]])
	.action_({ |button|
		tempOneCopy=sequences[in][currentCluster].postln;
		// seqs[currentCluster]=(m[i].value*255).round;
		// a[i].postln.string_((m[i].value*255).round.asString.postln);
	});
	Button(w, 50@20).states_([["paste", Color.white, Color.black]])
	.action_({ |button|
		// sequences[in][currentCluster]=tempOneCopy/255;
		// tempOneCopy.postln;
		sequences[in][currentCluster]=tempOneCopy;
		getSeqs.value(currentCluster);
		// seqs[currentCluster]=(m[i].value*255).round;
		// a[i].postln.string_((m[i].value*255).round.asString.postln);
	});
	Button(w, 20@20).states_([["x", Color.white, Color.red]])
	.action_({ |button|
		"clear".postln;
		sequences[in][currentCluster] = {0}!size;
		getSeqs.value(currentCluster);
		// seqs.postln;


	});
	mt;
};
// load.value(0);
)
//FUNCS
// var setSeqs={|clust|
// 	var c =	(clust ).postln;
// 	sequences.do{|i|
// 		i[0];
//
//
// 	}
// 	sequences[c]=(m.bdrum.value*255).round.asInteger;
// 	sequences[c+1]=(m.sdrum.value*255).round.asInteger;
// 	sequences[c+2]=(m.hhats.value*255).round.asInteger;
// };

var setOneSeq={|clust, item, value|
	var c =	(clust * 3).postln;
	seqs[c]=(value*255).round.asInteger;
};
var getSeqs={|clust, seq|
	var c =	(clust * 3).postln;

	m.bdrum.value=seqs[c+0]/255;
	m.sdrum.value=seqs[c+1]/255;
	m.hhats.value=seqs[c+2]/255;
};
var load={|preset|
	var fileToLoad=(presetNames[preset].fullPath++presetNames[preset].folderName++".preset").postln;
	seqs = Object.readArchive(fileToLoad);
	getSeqs.value(currentCluster);

};
var save={
	var path= presetNames[currentPreset].fullPath;
	var bool =itemsFolder.detect({|i| i==t.string}).notNil;
	var newPath;
	setSeqs.value(0);
	if(bool.postln==false,{File.mkdir(folder.fullPath++"/"++t.string);});
	seqs.writeArchive((folder.fullPath++"/"++t.string++"/"++t.string++".preset").standardizePath);
	f = File.new((folder.fullPath++"/"++t.string++"/"++t.string++".txt").standardizePath, "w");
	seqs.postln;
	f.putString(seqs.asCompileString);
	f.close;
	refresh.value();

};
var refresh={
	presetNames= folder.folders;
	itemsFolder = presetNames.collect{|i| i.folderName}.postln;
	pop.items=(itemsFolder);
};

///dicts


//window----
w = Window("ORSINI DRUMMER FUCKER", 900@800, resizable: true).front;
w.view.decorator = FlowLayout(w.view.bounds);
t=TextField(w,600@20).string_(presetNames[currentPreset].folderName);
Button(w, 100@20).states_([["save", Color.white, Color.black]])
.action_({ |button|
	"save".postln;
	save.value();
	setSeqs.value(currentCluster);
	// seqs.postln;


});

pop=PopUpMenu(w, 120@20).items_(itemsFolder).action_{|menu|

	t.string_(menu.item);
	load.value(menu.value);

};
///MULTIS
instruments.do{|i|
	var mt = MultiSliderView(w, Rect(0, 0, 890, 100));
	mt.value_(Array.fill(size, {0.0}));
	mt.isFilled_(true); // width in pixels of each stick
	mt.indexThumbSize_((900-(32*4)/33)); // spacing on the value axis
	mt.gap_(4);
	mt.action_({|multi|
		setOneSeq.value(multi.value, i);

	});
	32.do{| i |
		StaticText(w, (890/38)@30).string_(i+1).align_(\center)};
	// g = TextField(w, Rect(10, 10, 890, 40));
	f=Button(w, 890@20).states_([["  ", Color.white, Color.black]])
	.action_({ |button|
		seqs[currentCluster]=(m[i].value*255).round;
		a[i].postln.string_((m[i].value*255).round.asString.postln);
	});



};
9.do{|cluster|
	c=Button(w, 100@20).states_([["request "++cluster, Color.white, Color.black]])
	.action_({ |button|
		getSeqs.value(cluster);
		currentCluster=cluster.postln;
		// h = Object.readArchive(prstPth.fullPath);
		// c =	(cluster * 3).postln;
		/*m.bdrum.value=h[c+0]/255;
		m.sdrum.value=h[c+1]/255;
		m.hhats.value=h[c+2]/255;*/
	});
};
load.value(0);
getSeqs.value(currentCluster);
)