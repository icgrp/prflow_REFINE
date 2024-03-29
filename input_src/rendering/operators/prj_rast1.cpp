#include "../host/typedefs.h"


int check_clockwise( Triangle_2D triangle_2d )
{
  int cw;

  cw = (triangle_2d.x2 - triangle_2d.x0) * (triangle_2d.y1 - triangle_2d.y0)
       - (triangle_2d.y2 - triangle_2d.y0) * (triangle_2d.x1 - triangle_2d.x0);

  return cw;
}


// swap (x0, y0) (x1, y1) of a Triangle_2D
void clockwise_vertices( Triangle_2D *triangle_2d )
{

  bit8 tmp_x, tmp_y;

  tmp_x = triangle_2d->x0;
  tmp_y = triangle_2d->y0;

  triangle_2d->x0 = triangle_2d->x1;
  triangle_2d->y0 = triangle_2d->y1;

  triangle_2d->x1 = tmp_x;
  triangle_2d->y1 = tmp_y;
}


bit8 find_min( bit8 in0, bit8 in1, bit8 in2 )
{
  if (in0 < in1)
  {
    if (in0 < in2)
      return in0;
    else
      return in2;
  }
  else
  {
    if (in1 < in2)
      return in1;
    else
      return in2;
  }
}


// find the max from 3 integers
bit8 find_max( bit8 in0, bit8 in1, bit8 in2 )
{
  if (in0 > in1)
  {
    if (in0 > in2)
      return in0;
    else
      return in2;
  }
  else
  {
    if (in1 > in2)
      return in1;
    else
      return in2;
  }
}


void data_transfer (
    hls::stream<ap_uint<256>> & Input_1,
    hls::stream<ap_uint<128>> & Output_1)

{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1
  static ap_uint<256> in_tmp;
  ap_uint<128> out_tmp;
  static ap_uint<8> counter = 0;

  if (counter == 0) in_tmp = Input_1.read();
  Output_1.write(in_tmp(counter*128+127, counter*128)); // match the number of reads in p_r1_module
  if(counter == 1) counter = 0;
  else counter++;


}

// project a 3D triangle to a 2D triangle
void projection_i1 (
    bit32 input_lo,
    bit32 input_mi,
    bit32 input_hi,
    Triangle_2D *triangle_2d
    )
{
  #pragma HLS INLINE off
  Triangle_3D triangle_3d;
  // Setting camera to (0,0,-1), the canvas at z=0 plane
  // The 3D model lies in z>0 space
  // The coordinate on canvas is proportional to the corresponding coordinate
  // on space

  bit2 angle = 0;
  triangle_3d.x0(7, 0) = input_lo( 7,  0);
  triangle_3d.y0(7, 0) = input_lo(15,  8);
  triangle_3d.z0(7, 0) = input_lo(23, 16);
  triangle_3d.x1(7, 0) = input_lo(31, 24);
  triangle_3d.y1(7, 0) = input_mi( 7,  0);
  triangle_3d.z1(7, 0) = input_mi(15,  8);
  triangle_3d.x2(7, 0) = input_mi(23, 16);
  triangle_3d.y2(7, 0) = input_mi(31, 24);
  triangle_3d.z2(7, 0) = input_hi( 7,  0);

  if(angle == 0)
  {
    triangle_2d->x0 = triangle_3d.x0;
    triangle_2d->y0 = triangle_3d.y0;
    triangle_2d->x1 = triangle_3d.x1;
    triangle_2d->y1 = triangle_3d.y1;
    triangle_2d->x2 = triangle_3d.x2;
    triangle_2d->y2 = triangle_3d.y2;
    triangle_2d->z  = triangle_3d.z0 / 3 + triangle_3d.z1 / 3 + triangle_3d.z2 / 3;
  }

  else if(angle == 1)
  {
    triangle_2d->x0 = triangle_3d.x0;
    triangle_2d->y0 = triangle_3d.z0;
    triangle_2d->x1 = triangle_3d.x1;
    triangle_2d->y1 = triangle_3d.z1;
    triangle_2d->x2 = triangle_3d.x2;
    triangle_2d->y2 = triangle_3d.z2;
    triangle_2d->z  = triangle_3d.y0 / 3 + triangle_3d.y1 / 3 + triangle_3d.y2 / 3;
  }

  else if(angle == 2)
  {
    triangle_2d->x0 = triangle_3d.z0;
    triangle_2d->y0 = triangle_3d.y0;
    triangle_2d->x1 = triangle_3d.z1;
    triangle_2d->y1 = triangle_3d.y1;
    triangle_2d->x2 = triangle_3d.z2;
    triangle_2d->y2 = triangle_3d.y2;
    triangle_2d->z  = triangle_3d.x0 / 3 + triangle_3d.x1 / 3 + triangle_3d.x2 / 3;
  }
}


// calculate bounding box for a 2D triangle
void rasterization1_i1 (
    Triangle_2D triangle_2d,
    hls::stream<ap_uint<32> > & Output_1)
{
  Triangle_2D triangle_2d_same;
  static bit8 max_min[5]={0, 0, 0, 0, 0};
  static bit16 max_index[1]={0};


  #pragma HLS INLINE off
  // clockwise the vertices of input 2d triangle
  if ( check_clockwise( triangle_2d ) == 0 ){
    bit32 tmp;
    tmp(7,0) = 1;
    tmp(15, 8) = triangle_2d_same.x0;
    tmp(23,16) = triangle_2d_same.y0;
    tmp(31,24) = triangle_2d_same.x1;
    Output_1.write(tmp);

    tmp(7,0) = triangle_2d_same.y1;
    tmp(15, 8) = triangle_2d_same.x2;
    tmp(23,16) = triangle_2d_same.y2;
    tmp(31,24) = triangle_2d_same.z;
    Output_1.write(tmp);

    tmp(15,0) = max_index[0];
    tmp(23,16) = max_min[0];
    tmp(31,24) = max_min[1];
    Output_1.write(tmp);

    tmp(7,0) = max_min[2];
    tmp(15, 8) = max_min[3];
    tmp(23,16) = max_min[4];
    tmp(31,24) = 0;
    Output_1.write(tmp);

    return;
  }

  if ( check_clockwise( triangle_2d ) < 0 )
    clockwise_vertices( &triangle_2d );

  // copy the same 2D triangle
  triangle_2d_same.x0 = triangle_2d.x0;
  triangle_2d_same.y0 = triangle_2d.y0;
  triangle_2d_same.x1 = triangle_2d.x1;
  triangle_2d_same.y1 = triangle_2d.y1;
  triangle_2d_same.x2 = triangle_2d.x2;
  triangle_2d_same.y2 = triangle_2d.y2;
  triangle_2d_same.z  = triangle_2d.z ;

  // find the rectangle bounds of 2D triangles
  max_min[0] = find_min( triangle_2d.x0, triangle_2d.x1, triangle_2d.x2 );
  max_min[1] = find_max( triangle_2d.x0, triangle_2d.x1, triangle_2d.x2 );
  max_min[2] = find_min( triangle_2d.y0, triangle_2d.y1, triangle_2d.y2 );
  max_min[3] = find_max( triangle_2d.y0, triangle_2d.y1, triangle_2d.y2 );
  max_min[4] = max_min[1] - max_min[0];

  // calculate index for searching pixels
  max_index[0] = (max_min[1] - max_min[0]) * (max_min[3] - max_min[2]);
  bit32 tmp;

  tmp(7,0) = 0;
  tmp(15,8) = triangle_2d_same.x0;
  tmp(23,16) = triangle_2d_same.y0;
  tmp(31,24) = triangle_2d_same.x1;
  Output_1.write(tmp);

  tmp(7,0) = triangle_2d_same.y1;
  tmp(15,8) = triangle_2d_same.x2;
  tmp(23,16) = triangle_2d_same.y2;
  tmp(31,24) = triangle_2d_same.z;
  Output_1.write(tmp);

  tmp(15,0) = max_index[0];
  tmp(23,16) = max_min[0];
  tmp(31,24) = max_min[1];
  Output_1.write(tmp);

  tmp(7,0) = max_min[2];
  tmp(15,8) = max_min[3];
  tmp(23, 16) = max_min[4];
  tmp(31, 24) = 0;
  Output_1.write(tmp);

  return;
}


void p_r1_module (
    hls::stream<ap_uint<128>> & Input_1,
    hls::stream<ap_uint<32>> & Output_1
    )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

  bit32 input_lo;
  bit32 input_mi;
  bit32 input_hi;
  bit128 input_tmp;

  Triangle_2D triangle_2ds_1;

  input_tmp = Input_1.read();

  input_lo(31,0) = input_tmp(31,  0);
  input_mi(31,0) = input_tmp(63, 32);
  input_hi(31,0) = input_tmp(95, 64);
  projection_i1 (
    input_lo,
    input_mi,
    input_hi,
    &triangle_2ds_1);

  rasterization1_i1 (
    triangle_2ds_1,
    Output_1);

}

void prj_rast1 (
    hls::stream<ap_uint<256>> & Input_1,
    hls::stream<ap_uint<32>> & Output_1
    )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<128>> data_transfer_out("data_transfer_out_stream");

#pragma HLS dataflow
    data_transfer(Input_1, data_transfer_out);
    p_r1_module(data_transfer_out, Output_1);
}
