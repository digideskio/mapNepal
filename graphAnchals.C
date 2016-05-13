#include "Riostream.h"
#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"

#include <map>
#include <vector>

#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TGraph.h"
#include "TCanvas.h"


#include <fstream>
#include <sstream>
#include <string>

// Copied from Paul's code @ PLTOffline
void normalize(TGraph *g) {
  // Since TGraph doesn't include a Scale() function,
  // we have to modify the data in-place. This solution
  // is from Rene Brun himself!

  float s = 1.0/g->GetHistogram()->GetMaximum();
  float m = g->GetHistogram()->GetMinimum()*s;
  for (int i=0; i<g->GetN(); ++i)
    g->GetY()[i] *= s;

  g->SetMaximum(1.0);
  g->SetMinimum(m);
  return;
}

void graphAnchals(){

  //  gROOT->SetBatch(kTRUE);

  std::map<int, std::vector<double>> longitude;
  std::map<int, std::vector<double>> latitude;

  std::map<int, TGraph*> graphs;
  std::map<int, int> mapsize;



  TCanvas *c1 = new TCanvas("c1","A Simple Graph Example",200,10,700,500);
  c1->SetGrid();

  TMultiGraph *mg = new TMultiGraph();

  int begin =  4583210;
  int end = 4583224;

  int index = 1;

  for (Int_t iter = begin; iter < end; iter++) {

    stringstream filename;
    filename<< "./polyAnchals/poly_" <<iter << ".txt";
    temp = filename.str();
    std::ifstream infile(temp.c_str(), ios::in);

    if (!infile) { std::cerr << "Error opening file!\n"; return 1; }

    double a, b;


    while (infile >> a >> b) {
      //      std::cout << a << " " << b << std::endl;
      longitude[index].push_back(a);
      latitude[index].push_back(b);
    }
    mapsize[index] = longitude[index].size() % 100 + index / 14;

    std::cout << index << " " << longitude[index].size() << " " << mapsize[index]<< std::endl;
    //    Int_t palette[14];



    graphs[index] = new TGraph(longitude[index].size(),&longitude[index][0],&latitude[index][0]);

    //  normalize(graphs[index]);
    graphs[index]->SetMarkerColor(index);
    graphs[index]->SetFillColor(index);
    //graphs[index]->SetFillColorAlpha(kRed,mapsize[index]/300.);
    graphs[index]->SetFillStyle(1001+index);
    mg->Add(graphs[index]);

    index++;
  }

  mg->Draw("ACF");
  mg->SetTitle("14 Anchals -- Nepal");
  mg->GetXaxis()->SetTitle("Latitude");
  mg->GetYaxis()->SetTitle("Longitude");
  gPad->Modified();
  //  c1->BuildLegend();
  c1->Update();
  c1->Print("graphAnchals.gif");
  //  return ;
}
