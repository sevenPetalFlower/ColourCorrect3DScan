
save_filename = 'primaries.mat';
cs2000 = CS2000;
primaries = cs2000.measure;
save(save_filename, 'primaries');

fileName = 'Putt pass to Raw image';
cfaInfo = rawinfo(fileName);
aux = [primaries.color.XYZ];
wp = aux ./ aux(2);
colorInfo = cfaInfo.ColorInfo;
cam2xyzMat = colorInfo.CameraToXYZ
RGB_camera = cam2xyzMat \ wp;
wp_multipliers = 1./(RGB_camera ./ RGB_camera(2));