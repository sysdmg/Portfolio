document.addEventListener('DOMContentLoaded', () => {
    const imageUpload = document.getElementById('imageUpload');
    const resultSection = document.getElementById('resultSection');
    const originalImage = document.getElementById('originalImage');
    const paletteCanvas = document.getElementById('paletteCanvas');
    const colorCodes = document.getElementById('colorCodes');

    imageUpload.addEventListener('change', handleImageUpload);

    function handleImageUpload(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const img = new Image();
                img.onload = function() {
                    originalImage.src = img.src;
                    resultSection.style.display = 'flex';
                    generatePalette(img);
                };
                img.src = event.target.result;
            };
            reader.readAsDataURL(file);
        }
    }

    function generatePalette(img) {
        // Create a canvas to analyze the image
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // Resize large images for better performance
        const maxSize = 400;
        let width = img.width;
        let height = img.height;
        
        if (width > maxSize || height > maxSize) {
            const ratio = Math.min(maxSize / width, maxSize / height);
            width *= ratio;
            height *= ratio;
        }
        
        canvas.width = width;
        canvas.height = height;
        ctx.drawImage(img, 0, 0, width, height);

        // Get image data
        const imageData = ctx.getImageData(0, 0, width, height).data;
        const colors = [];
        
        // Sample pixels with dynamic spacing
        const sampleSize = Math.max(1, Math.floor((width * height) / 10000));
        
        for (let i = 0; i < imageData.length; i += 4 * sampleSize) {
            const r = imageData[i];
            const g = imageData[i + 1];
            const b = imageData[i + 2];
            
            // Convert to HSL for better color analysis
            const hsl = rgbToHsl(r, g, b);
            
            // Only add colors with sufficient saturation and luminance
            if (hsl[1] > 0.1 && hsl[2] > 0.1 && hsl[2] < 0.9) {
                colors.push([r, g, b, hsl]);
            }
        }

        // Cluster colors using k-means like approach
        const clusters = [];
        const numClusters = 8; // Extract more colors initially
        
        // Initialize clusters with evenly spaced colors
        for (let i = 0; i < numClusters && colors.length > 0; i++) {
            const index = Math.floor((colors.length / numClusters) * i);
            clusters.push({
                center: colors[index].slice(0, 3),
                colors: []
            });
        }

        // Assign colors to nearest cluster
        for (let i = 0; i < 5; i++) { // 5 iterations of refinement
            clusters.forEach(cluster => cluster.colors = []);
            
            colors.forEach(color => {
                let minDist = Infinity;
                let nearestCluster = clusters[0];
                
                clusters.forEach(cluster => {
                    const dist = colorDistance(color.slice(0, 3), cluster.center);
                    if (dist < minDist) {
                        minDist = dist;
                        nearestCluster = cluster;
                    }
                });
                
                nearestCluster.colors.push(color);
            });
            
            // Update cluster centers
            clusters.forEach(cluster => {
                if (cluster.colors.length > 0) {
                    cluster.center = cluster.colors.reduce((acc, curr) => {
                        return [acc[0] + curr[0], acc[1] + curr[1], acc[2] + curr[2]];
                    }, [0, 0, 0]).map(v => Math.round(v / cluster.colors.length));
                }
            });
        }

        // Sort clusters by size and color significance
        const sortedColors = clusters
            .filter(cluster => cluster.colors.length > 0)
            .sort((a, b) => {
                const aScore = getColorScore(a);
                const bScore = getColorScore(b);
                return bScore - aScore;
            })
            .map(cluster => cluster.center)
            .slice(0, 5);

        // Draw the palette
        drawPalette(sortedColors);
        displayColorCodes(sortedColors);
    }

    function drawPalette(colors) {
        const ctx = paletteCanvas.getContext('2d');
        const width = paletteCanvas.width;
        const height = paletteCanvas.height;
        const colorWidth = width / colors.length;

        colors.forEach((color, i) => {
            ctx.fillStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
            ctx.fillRect(i * colorWidth, 0, colorWidth, height);
        });
    }

    function displayColorCodes(colors) {
        colorCodes.innerHTML = '';
        colors.forEach(color => {
            const hex = rgbToHex(color[0], color[1], color[2]);
            const div = document.createElement('div');
            div.className = 'color-code';
            div.textContent = hex;
            colorCodes.appendChild(div);
        });
    }

    function rgbToHex(r, g, b) {
        const toHex = (c) => {
            const hex = c.toString(16);
            return hex.length === 1 ? '0' + hex : hex;
        };
        return `#${toHex(r)}${toHex(g)}${toHex(b)}`.toUpperCase();
    }

    function rgbToHsl(r, g, b) {
        r /= 255;
        g /= 255;
        b /= 255;
        
        const max = Math.max(r, g, b);
        const min = Math.min(r, g, b);
        let h, s, l = (max + min) / 2;

        if (max === min) {
            h = s = 0;
        } else {
            const d = max - min;
            s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
            
            switch (max) {
                case r: h = (g - b) / d + (g < b ? 6 : 0); break;
                case g: h = (b - r) / d + 2; break;
                case b: h = (r - g) / d + 4; break;
            }
            
            h /= 6;
        }

        return [h, s, l];
    }

    function colorDistance(color1, color2) {
        // Calculate distance in Lab color space for better perceptual difference
        const labColor1 = rgbToLab(color1);
        const labColor2 = rgbToLab(color2);
        
        return Math.sqrt(
            Math.pow(labColor2[0] - labColor1[0], 2) +
            Math.pow(labColor2[1] - labColor1[1], 2) +
            Math.pow(labColor2[2] - labColor1[2], 2)
        );
    }

    function rgbToLab(rgb) {
        // Convert RGB to XYZ
        let r = rgb[0] / 255;
        let g = rgb[1] / 255;
        let b = rgb[2] / 255;

        r = r > 0.04045 ? Math.pow((r + 0.055) / 1.055, 2.4) : r / 12.92;
        g = g > 0.04045 ? Math.pow((g + 0.055) / 1.055, 2.4) : g / 12.92;
        b = b > 0.04045 ? Math.pow((b + 0.055) / 1.055, 2.4) : b / 12.92;

        const x = (r * 0.4124 + g * 0.3576 + b * 0.1805) * 100;
        const y = (r * 0.2126 + g * 0.7152 + b * 0.0722) * 100;
        const z = (r * 0.0193 + g * 0.1192 + b * 0.9505) * 100;

        // Convert XYZ to Lab
        const xn = 95.047;
        const yn = 100.000;
        const zn = 108.883;

        const fx = x / xn > 0.008856 ? Math.pow(x / xn, 1/3) : (7.787 * x / xn) + 16/116;
        const fy = y / yn > 0.008856 ? Math.pow(y / yn, 1/3) : (7.787 * y / yn) + 16/116;
        const fz = z / zn > 0.008856 ? Math.pow(z / zn, 1/3) : (7.787 * z / zn) + 16/116;

        return [
            (116 * fy) - 16,
            500 * (fx - fy),
            200 * (fy - fz)
        ];
    }

    function getColorScore(cluster) {
        const [r, g, b] = cluster.center;
        const hsl = rgbToHsl(r, g, b);
        const saturation = hsl[1];
        const luminance = hsl[2];
        
        // Consider both cluster size and color properties
        return (
            cluster.colors.length * 
            (0.5 + saturation) * // Favor saturated colors
            (1 - Math.abs(luminance - 0.5)) // Favor mid-range luminance
        );
    }
});