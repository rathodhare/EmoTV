#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <iostream>
#include <math.h>
#include <stdio.h>
#include <time.h>
#include <istream>
#include <fstream>
#include <ctime>
#include <string.h>

using namespace cv;
using namespace std;
 
Mat colour_asphalt_thresholding(Mat img,int thresh_arg)
{
	int I,J;
	I=img.rows;
	J=img.cols;
	
	Mat asphalt=Mat::zeros(I,J, CV_8UC1 );	
	
	int grey_thresh=thresh_arg;
	for(int i=0;i<I;i++)
		{
		for(int j=0;j<J;j++)
			{	
				int b,g,r;

				b=img.at<cv::Vec3b>(i,j)[0];
				g=img.at<cv::Vec3b>(i,j)[1];
				r=img.at<cv::Vec3b>(i,j)[2];
			if(abs(b-g)<grey_thresh&&abs(g-r)<grey_thresh&&abs(r-b)<grey_thresh)											
				asphalt.at<uchar>(i,j)=1;
				
			}
		}		
return asphalt;
}


 variance_filter(int* r,int* g,int* b,int thresh_var,int ws,int size,int I)
{
 int J=size/I; 	
 int sb,sg,sr; 
 int *vary;
 int *img_b,*img_g,*img_r;

 vary=new int[size];
 img_b=new int[size];
 img_g=new int[size];
 img_r=new int[szie];

 int variance_thresh=thresh_var;
 float  sumb=0,sumg=0,sumr=0;  // sumx: sum of pixel values around the pixel of intrest
 int pixel_count=0;
 int window_size=ws;  // this is half the window size 

 int v=blockIdx.x+window_size, u=blockIdx.x-window_size;
 int row=(blockIdx.x-(blockIdx.x%I))/I;
 int col=blockIdx.x%I;
 float local_variance_b=0,local_variance_g=0,local_variance_r=0;
 for(int k=row-window_size;k<row+window_size && k>=0 && k<I;k++)
 {
 	for(int l=col-window_size;l<col+window_size && l>=0 && l<J; l++)
 	{
 		pixel_count+=1;
 		sumb+=*(b+k*J + l);
 		sumg+=*(g+k*J + l);
 		sumr+=*(r+k*J + l);
 	}
 	__syncthreads();
 } 
 __syncthreads();
for(int k=row-window_size;k<row+window_size && k>=0 && k<I;k++)
 {
 	for(int l=col-window_size;l<col+window_size && l>=0 && l<J; l++)
 	{
 		sb=*(b+k*J + l);
        sg=*(g+k*J + l);
        sr=*(r+k*J + l);

        local_variance_b+=(sumb-sb)*(sumb-sb); 
        local_variance_g+=(sumb-sg)*(sumb-sg);
        local_variance_r+=(sumb-sr)*(sumb-sr);
    }
    __syncthreads();
 }
 __syncthreads();
 local_variance_b=sqrt(local_variance_b)/pixel_count;
 local_variance_g=sqrt(local_variance_g)/pixel_count;
 local_variance_r=sqrt(local_variance_r)/pixel_count;
 
 if(local_variance_b<variance_thresh||local_variance_g<variance_thresh||local_variance_r<variance_thresh)
    *(vary+i*J + j)=0;
 else
    *(vary+i*J + j)=255;
				
 local_variance_b=0;
 local_variance_g=0;
 local_variance_r=0;

 sumb=0;
 sumg=0;
 sumr=0;

 pixel_count=0;		

delete vary;
delete img_r;
delete img_b;
delete img_g;

return vary;
}

Mat histogram_equalization_colored(Mat img)
{
	Mat B,G,R;

	int I,J;
	I=img.rows;
	J=img.cols;

	cvtColor(img,img,CV_BGR2YCrCb);

	Mat hist_equal=Mat::zeros(I,J,CV_8UC3);
	Mat img_split[3];
	split(img,img_split);

	cv::Ptr<cv::CLAHE> clahe=cv::createCLAHE();
	clahe->setClipLimit(4);
	clahe->apply(img_split[0],B);

	for(int i=0;i<I;i++)
		{
		for(int j=0;j<J;j++)
			{	
				
				hist_equal.at<Vec3b>(i,j)[0]=B.at<uchar>(i,j);
				hist_equal.at<Vec3b>(i,j)[1]=img_split[1].at<uchar>(i,j);
				hist_equal.at<Vec3b>(i,j)[2]=img_split[2].at<uchar>(i,j);
			
			}			
		}	

	cvtColor(hist_equal,hist_equal,CV_YCrCb2BGR);
	return hist_equal ;
}

int luminosity_correct(Mat img)
{
	Mat B,G,R;

	int I,J;
	I=img.rows;
	J=img.cols;
	Mat cpy;
	cvtColor(img,cpy,CV_BGR2YCrCb);

	Mat hist_equal=Mat::zeros(I,J,CV_8UC3);
	Mat img_split[3];
	split(cpy,img_split);

	long int lum=0;

	for(int i=0;i<I;i++)
		{
		for(int j=0;j<J;j++)
			{	
				
				lum+=img_split[0].at<uchar>(i,j);
				
			}			
		}	

	return lum/(I*J);
}

Mat canny_edges_func(Mat img,int filter_size)
{
	Mat split_img[3];
	split(img,split_img);
	Mat edges[3];

	int a=filter_size;

	Canny(split_img[0],edges[0],a,3*a,3);
	Canny(split_img[2],edges[2],a,3*a,3);
	Canny(split_img[1],edges[1],a,3*a,3);

	Mat edgesf;

	addWeighted(edges[0],1,edges[1],1,0,edgesf);
	addWeighted(edges[2],1,edgesf,1,0,edgesf);


	return edgesf;

}
Mat invert(Mat img)
{
	int I,J;
	I=img.rows;
	J=img.cols;

	for(int i=0;i<I;i++)
	{
		for(int j=0;j<J;j++)
		{
			if(img.at<uchar>(i,j)==255)
				img.at<uchar>(i,j)=0;
			else
				img.at<uchar>(i,j)=255;
		}
	}

	return img;
}

Mat lane_marker_detect(Mat img,int color_thresh)
{
	int I,J;
	I=img.rows;
	J=img.cols;

	Mat lanes=Mat::zeros(I,J,CV_8UC1);

	for(int i=0;i<I;i++)
	{
		for(int j=0;j<J;j++)
		{
			if(img.at<Vec3b>(i,j)[0]>color_thresh&&img.at<Vec3b>(i,j)[1]>color_thresh&&img.at<Vec3b>(i,j)[2]>color_thresh)
				lanes.at<uchar>(i,j)=255;
			else
				lanes.at<uchar>(i,j)=0;
		}
	}


	return lanes;

}
float type_2_error(Mat img,Mat ref)
{
	int I,J;
	I=img.rows;
	J=img.cols;
	float counter=0;
	float correct=0;

	for(int i=0;i<I;i++)
	{
		for(int j=0;j<J;j++)
		{
			int b;
			b=ref.at<uchar>(i,j);
			if(b==255)
			{
				counter+=1;
				int z;
				z=img.at<uchar>(i,j);
				if(z==0)
				{
					correct+=1;
				}
			}
		}
	}

	return 100*correct/counter;
}

Mat region_of_intrest(int I,int J,float slope)
{
	Mat reg=Mat::zeros(I,J,CV_8UC1);

	for(float i=0;i<I;i++)
	{
		for(float j=0;j<J;j++)
		{
			if(i>0.4*I&&(i-slope*j>0.6*I)&&(i+slope*(j-J)>0.6*I))
				reg.at<uchar>(i,j)=1;
		}
	}
	return reg;
}

/*
Mat canny_to_lanes(Mat img)
{
	int I,J;
	I=img.rows;
	J=img.cols;

	Mat canny_road[5];

	int xcorr[5]={0.2*J,0.4*J,0.5*J,0.6*J,0.8*J};
	int ycorr[5]={0,0,0,0,0};

	for(int k=0;k<5;k++)
	{
		canny_road[k]=canny_roadpointcall(xcorr[k],ycorr[k],img);
		addWeighted(canny_road[k],1,canny_road[0],1,0,canny_road[0]);
	}
	
return canny_road[0];
}
*/

int main()
{	VideoCapture vc;
	Mat rgb,var;
	int* r,g,b,d_r,d_g,d_b;
	while(vc.open("to.MOV"))
	{	
		
		Mat img_bw,out;
		//cout<<vc.retrieve(img,0)<<endl;
		while(vc.read(img_bw))
		{
			float lum;
			int size=img_bw.rows()*img_bw.cols()
            r=new int[size];
            g=new int[size];
            b=new int[size];
            int k=0;
            for(int i=0;i<img_bw.rows();i++)
            {
            	for(int j=0;j<img_bw.cols();j++)
            	{
                    *(r+k)=img.at<cv::Vec3b>(i,j)[0];
            	    *(g+k)=img.at<cv::Vec3b>(i,j)[1];
            	    *(b+k)=img.at<cv::Vec3b>(i,j)[2];
            	    k++;
            	}
            }
            cudaMalloc((void**)&d_r,size);
            cudaMalloc((void**)&d_g,size);
            cudaMalloc((void**)&d_b,size);
            cudaMemcpy(d_r,r,size,cudaMemcpyHostToDevice);
            cudaMemcpy(d_g,g,size,cudaMemcpyHostToDevice);
            cudaMemcpy(d_b,b,size,cudaMemcpyHostToDevice);
            int* out=variance_filter<<<size,1>>>(d_r,d_g,d_b,500,3,size,img_bw.rows());
            for(int i=0;i<img_bw.rows();i++)
            {
            	for(int j=0;j<img_bw.cols();j++)
            	{
            		var.at<uchar>(i,j) = *(out+i*J + j);
            	}
            }
            cudaFree(d_r);
            cudaFree(d_g);
            cudaFree(d_b);
            free(r);
            free(g);
            free(b);
      		//img_bw=imread("pp.png",1);
			//img_bw=histogram_equalization_colored(img_bw);
			//img_bw=histogram_equalization_colored(img_bw);
			//rgb=colour_asphalt_thresholding(img_bw,15);
			//var=variance_filter(img_bw,500,3);
			lum=luminosity_correct(img_bw);
			lum=130/lum;
			img_bw=img_bw*lum;
			//out=var.mul(rgb);
			//imshow("original",img_bw);
			//imshow("output",out);
			imshow("var",img_bw);
			waitKey(1);
			
		}
	}
return 0;

}
