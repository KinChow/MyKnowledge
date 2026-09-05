---
archive_policy: text-only
attachments:
- filename: web-multimedia-auto-white-balance.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:02a71ac8fbaf8297e3511a58c0ffad726e5a006f5c7af7207b4026f28f4c064e
confidentiality: public
domain: multimedia
evidence_items:
- evidence_id: evidence-33a2fc20ca9d
  position:
    end: 478
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:7e0cb5e306a6e380b1783e6e68bd765bdf81e9045ea268941f0a7497db56ba32
  selector:
    exact: In photography and image processing, color balance is the global adjustment
      of the intensities of the colors (typically red, green, and blue primary colors).
      An important goal of this adjustment is to render specific colors – particularly
      neutral colors like white or grey – correctly. Hence, the general method is
      sometimes called gray balance, neutral balance, or white balance. Color balance
      changes the overall mixture of colors in an image and is used for color correction.
    prefix: ''
    suffix: ' Generalized versions of color b'
    type: TextQuoteSelector
  selector_sha256: sha256:cf612ddbccdad335d3126825fb5bcdebd7837c5c0abcb207e12637375f5c1dce
  snapshot_sha256: sha256:80e333e65c05394fb50eab84820fbaef6369f4f80d145d36fca57377d73bf175
extractor: trafilatura/2.2.0
id: web-multimedia-auto-white-balance
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/02a71ac8fbaf8297e3511a58c0ffad726e5a006f5c7af7207b4026f28f4c064e.html
  sha256: sha256:02a71ac8fbaf8297e3511a58c0ffad726e5a006f5c7af7207b4026f28f4c064e
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://en.wikipedia.org/wiki/Color_balance
  url: https://en.wikipedia.org/wiki/Color_balance
schema_version: source/v1
snapshot_sha256: sha256:80e333e65c05394fb50eab84820fbaef6369f4f80d145d36fca57377d73bf175
source_type: doc
vault_id: public
---
In photography and image processing, color balance is the global adjustment of the intensities of the colors (typically red, green, and blue primary colors). An important goal of this adjustment is to render specific colors – particularly neutral colors like white or grey – correctly. Hence, the general method is sometimes called gray balance, neutral balance, or white balance. Color balance changes the overall mixture of colors in an image and is used for color correction. Generalized versions of color balance are used to correct colors other than neutrals or to deliberately change them for effect. White balance is one of the most common kinds of balancing, and is when colors are adjusted to make a white object (such as a piece of paper or a wall) appear white and not a shade of any other colour.
Image data acquired by sensors – either film or electronic image sensors – must be transformed from the acquired values to new values that are appropriate for color reproduction or display. Several aspects of the acquisition and display process make such color correction essential – including that the acquisition sensors do not match the sensors in the human eye, that the properties of the display medium must be accounted for, and that the ambient viewing conditions of the acquisition differ from the display viewing conditions.
The color balance operations in popular image editing applications usually operate directly on the red, green, and blue channel pixel values,[1][2] without respect to any color sensing or reproduction model. In film photography, color balance is typically achieved by using color correction filters over the lights or on the camera lens.[3]
Sometimes the adjustment to keep neutrals neutral is called white balance, and the phrase color balance refers to the adjustment that in addition makes other colors in a displayed image appear to have the same general appearance as the colors in an original scene.[4] It is particularly important that neutral (gray, neutral, white) colors in a scene appear neutral in the reproduction.[5]
Humans relate to flesh tones more critically than other colors. Trees, grass and sky can all be off without concern, but if human flesh tones are 'off' then the human subject can look sick or dead. To address this critical color balance issue, the tri-color primaries themselves are formulated to not balance as a true neutral color. The purpose of this color primary imbalance is to more faithfully reproduce the flesh tones through the entire brightness range.
Most digital cameras have means to select color correction based on the type of scene lighting, using either manual lighting selection, automatic white balance, or custom white balance.[6] The algorithms for these processes perform generalized chromatic adaptation.
Many methods exist for color balancing. Setting a button on a camera is a way for the user to indicate to the processor the nature of the scene lighting. Another option on some cameras is a button which one may press when the camera is pointed at a gray card or other neutral colored object. This captures an image of the ambient light, which enables a digital camera to set the correct color balance for that light.
There is a large literature on how one might estimate the ambient lighting from the camera data and then use this information to transform the image data. A variety of algorithms have been proposed, and the quality of these has been debated. A few examples and examination of the references therein will lead the reader to many others. Examples are Retinex, an artificial neural network[7] or a Bayesian method.[8]
Color balancing an image affects not only the neutrals, but other colors as well. An image that is not color balanced is said to have a color cast, as everything in the image appears to have been shifted towards one color.[9][page needed] Color balancing may be thought in terms of removing this color cast.
Color balance is also related to color constancy. Algorithms and techniques used to attain color constancy are frequently used for color balancing, as well. Color constancy is, in turn, related to chromatic adaptation. Conceptually, color balancing consists of two steps: first, determining the illuminant under which an image was captured; and second, scaling the components (e.g., R, G, and B) of the image or otherwise transforming the components so they conform to the viewing illuminant.
Viggiano found that white balancing in the camera's native RGB color model tended to produce less color inconstancy (i.e., less distortion of the colors) than in monitor RGB for over 4000 hypothetical sets of camera sensitivities.[10] This difference typically amounted to a factor of more than two in favor of camera RGB. This means that it is advantageous to get color balance right at the time an image is captured, rather than edit later on a monitor. If one must color balance later, balancing the raw image data will tend to produce less distortion of chromatic colors than balancing in monitor RGB.
Color balancing is sometimes performed on a three-component image (e.g., RGB) using a 3x3 matrix. This type of transformation is appropriate if the image was captured using the wrong white balance setting on a digital camera, or through a color filter. Changing the color balance of an image can improve classifier results on a trained ML model.
In principle, one wants to scale all relative luminances in an image so that objects which are believed to be neutral appear so. If, say, a surface with was believed to be a white object, and if 255 is the count which corresponds to white, one could multiply all red values by 255/240. Doing analogously for green and blue would result, at least in theory, in a color balanced image. In this type of transformation the 3x3 matrix is a diagonal matrix.
where , , and are the color balanced red, green, and blue components of a pixel in the image; , , and are the red, green, and blue components of the image before color balancing, and , , and are the red, green, and blue components of a pixel which is believed to be a white surface in the image before color balancing. This is a simple scaling of the red, green, and blue channels, and is why color balance tools in Photoshop have a white eyedropper tool. It has been demonstrated that performing the white balancing in the phosphor set assumed by sRGB tends to produce large errors in chromatic colors, even though it can render the neutral surfaces perfectly neutral.[10]
If the image may be transformed into CIE XYZ tristimulus values, the color balancing may be performed there. This has been termed a "wrong von Kries" transformation.[11][12] Although it has been demonstrated to offer usually poorer results than balancing in monitor RGB, it is mentioned here as a bridge to other things. Mathematically, one computes:
where , , and are the color-balanced tristimulus values; , , and are the tristimulus values of the viewing illuminant (the white point to which the image is being transformed to conform to); , , and are the tristimulus values of an object believed to be white in the un-color-balanced image, and , , and are the tristimulus values of a pixel in the un-color-balanced image. If the tristimulus values of the monitor primaries are in a matrix so that:
where , , and are the un-gamma corrected monitor RGB, one may use:
Johannes von Kries, whose theory of rods and three color-sensitive cone types in the retina has survived as the dominant explanation of color sensation for over 100 years, motivated the method of converting color to the LMS color space, representing the effective stimuli for the Long-, Medium-, and Short-wavelength cone types that are modeled as adapting independently. A 3x3 matrix converts RGB or XYZ to LMS, and then the three LMS primary values are scaled to balance the neutral; the color can then be converted back to the desired final color space:[13]
where , , and are the color-balanced LMS cone tristimulus values; , , and are the tristimulus values of an object believed to be white in the un-color-balanced image, and , , and are the tristimulus values of a pixel in the un-color-balanced image.
Matrices to convert to LMS space were not specified by von Kries, but can be derived from CIE color matching functions and LMS color matching functions when the latter are specified; matrices can also be found in reference books.[13]
By Viggiano's measure, and using his model of gaussian camera spectral sensitivities, most camera RGB spaces performed better than either monitor RGB or XYZ.[10] If the camera's raw RGB values are known, one may use the 3x3 diagonal matrix:
and then convert to a working RGB space such as sRGB or Adobe RGB after balancing.
Comparisons of images balanced by diagonal transforms in a number of different RGB spaces have identified several such spaces that work better than others, and better than camera or monitor spaces, for chromatic adaptation, as measured by several color appearance models; the systems that performed statistically as well as the best on the majority of the image test sets used were the "Sharp", "Bradford", "CMCCAT", and "ROMM" spaces.[14]
The best color matrix for adapting to a change in illuminant is not necessarily a diagonal matrix in a fixed color space. It has long been known that if the space of illuminants can be described as a linear model with N basis terms, the proper color transformation will be the weighted sum of N fixed linear transformations, not necessarily consistently diagonalizable.[15]
- ↑ Phyllis Davis (2000). The Gimp for Linux and Unix. Peachpit Press. p. 134. ISBN 978-0-201-70253-8.
- ↑ Adobe Creative Team (2000). Adobe Photoshop 6.0. Adobe Press. p. 278. ISBN 978-0-201-71016-8.[need quotation to verify]
- ↑ Blain Brown (2002). Cinematography: Theory and Practice : Imagemaking for Cinematographers, Directors, and Videographers. Focal Press. p. 170. ISBN 978-0-240-80500-9.
- ↑ Hsien-Che Lee (2005). Introduction to Color Imaging Science. Cambridge University Press. p. 450. ISBN 978-0-521-84388-1.
- ↑ White Balance. Nikon Digital. Retrieved October 12, 2016
- ↑ Afifi, Mahmoud; Price, Brian; Cohen, Scott; Brown, Michael S (2019). "When Color Constancy Goes Wrong: Correcting Improperly White-Balanced Images" (PDF). 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). pp. 1535–1544. doi:10.1109/cvpr.2019.00163. ISBN 978-1-7281-3293-8. S2CID 196195956.
- ↑ Brian Funt, Vlad Cardei, and Kobus Barnard, "Learning color constancy", in Proceedings of the Fourth IS&T/SID Color Imaging Conference, pp. 58–60 (1996).
- ↑ Graham Finlayson; Paul M. Hubel; Steven Hordley (November 2001). "Color by correlation: a simple, unifying framework for color constancy" (PDF). IEEE Transactions on Pattern Analysis and Machine Intelligence. 23 (11): 1209–21. Bibcode:2001ITPAM..23.1209F. CiteSeerX 10.1.1.133.2101. doi:10.1109/34.969113. {{cite journal}} : Cite uses deprecated parameter|citeseerx= (help)
- ↑ John A C Yule, Principles of Color Reproduction. New York: Wiley, 1967.
- 1 2 3 Viggiano, J A Stephen (2004). "Comparison of the accuracy of different white-balancing options as quantified by their color constancy". In Blouke, Morley M; Sampat, Nitin; Motta, Ricardo J (eds.). Sensors and Camera Systems for Scientific, Industrial, and Digital Photography Applications V. Vol. 5301. pp. 323–333. doi:10.1117/12.524922. S2CID 8971750.
- ↑ Heinz Terstiege (1972). "Chromatic adaptation: a state-of-the-art report". Journal of Color Appearance. 1 (4): 19–23 (cont. 40).
- ↑ Mark D Fairchild, Color Appearance Models. Reading, MA: Addison-Wesley, 1998.
- 1 2 Gaurav Sharma (2003). Digital Color Imaging Handbook. CRC Press. p. 153. ISBN 978-0-8493-0900-7.
- ↑ Sabine Süsstrunk; Jack Holm; Graham D. Finlayson (January 2001). Eschbach, Reiner; Marcu, Gabriel G. (eds.). "Chromatic Adaptation Performance of Different RGB Sensors". IS&T/SPIE Electronic Imaging. Color Imaging: Device-Independent Color, Color Hardcopy, and Graphic Arts VI. 4300: 172–183. doi:10.1117/12.410788. S2CID 8140548. Archived from the original on 2006-10-18. Retrieved 2009-03-20.
- ↑ Laurence T. Maloney; Brain A. Wandell (1987). "Color constancy: a method for recovering surface spectral reflectance". In Martin A. Fischler; Oscar Firschein (eds.). Readings in Computer Vision. Morgan-Kaufmann. ISBN 978-0-934613-33-0.
- 1 2 "photoskop: Interactive Photography Lessons". April 25, 2015.
- White Balance - Intro at nikondigital.org
- photoskop: Interactive Photography Lessons - Interactive White Balance
- Understanding White Balance - Tutorial
- Affine color balance with saturation, with code and on-line demonstration
- Getting the White Balance Right for Neutral Colors - Photography Tutorial