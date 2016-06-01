#!opt/local/bin/perl

# anchals node begin to end
i=4583210; while [[ $i -le 4583223 ]];

#grab relational info for this node
do { wget -O ./temp/temp_$i.osm "http://overpass-api.de/api/interpreter?data=(rel($i);>);out;";
     # convert it to coordinates
     perl ./rel2poly.pl ./temp/temp_$i.osm > ./temp/temp_$i.txt
     # reduce datapoints, also filters first 3 lines containing text
     awk 'NR%3==0 && NF>=2' ./temp/temp_$i.txt > ./polyAnchals/poly_$i.txt
     # removes last line END, needs that extra ''. Not tested for other platforms
     #sed -i '' '$ d' ./polyAnchals/poly_$i.txt
     #sed -i '' '/END/d' ./polyAnchals/poly_$i.txt
     #sed -i '' '/polygon/d' ./polyAnchals/poly_$i.txt
     # now we only have poly co-ordinates which we can plot
     i=$(($i + 1));
};
done
