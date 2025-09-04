# Serial Section Overlay

![Alignment example on single-cell masks from three serial sections. Red dots highight all cells within 10 microns of randomly selected aligned pixels.](Serial_Section_Alignment.png)

This section covers we aligned single cell masks from serial sections. The steps we took were as follows:

1. Take only the pan-cytokeratin channel from the multi-stack tiffs, and train epithelial masks using Ilastik*. The epithelial masks are tiffs where pixels are "1" if the pixel is considered epithelial, and "0" for everything else.
2. Some of our TMAs were acquired in different orientations (ie 180 degree rotation). Cores were matched across slides and rotation was applied as necessary. The better the initial match, the better the alignment will work.
3. 





Citations: 
*Berg, S., Kutra, D., Kroeger, T., Straehle, C. N., Kausler, B. X., Haubold, C., Schiegg, M., Ales, J., Beier, T., Rudy, M., Eren, K., Cervantes, J. I., Xu, B., Beuttenmueller, F., Wolny, A., Zhang, C., Koethe, U., Hamprecht, F. A., & Kreshuk, A. (2019). ilastik: interactive machine learning for (bio)image analysis. Nature Methods, 16(12), 1226–1232.