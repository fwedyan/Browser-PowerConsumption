#!/usr/bin/env python3

ANIMATION_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Browser Animation Test</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: white;
            overflow: hidden;
        }
        #container {
            width: 100vw;
            height: 100vh;
            position: relative;
        }
        .animate-box {
            position: absolute;
            width: 50px;
            height: 50px;
            background-color: blue;
            border-radius: 5px;
            animation: move 4s infinite;
        }
        @keyframes move {
            0% { transform: translate(0, 0); background-color: blue; }
            25% { transform: translate(calc(100vw - 50px), 0); background-color: red; }
            50% { transform: translate(calc(100vw - 50px), calc(100vh - 50px)); background-color: green; }
            75% { transform: translate(0, calc(100vh - 50px)); background-color: orange; }
            100% { transform: translate(0, 0); background-color: blue; }
        }
    </style>
</head>
<body>
    <div id="container">
        <script>
            for (let i = 0; i < 100; i++) {
                const box = document.createElement('div');
                box.className = 'animate-box';
                box.style.animationDelay = (i * 0.1) + 's';
                document.getElementById('container').appendChild(box);
            }
        </script>
    </div>
</body>
</html>
"""

JS_COMPUTATION_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Browser CPU Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 0;
        }
        #status {
            font-size: 18px;
            margin-bottom: 20px;
        }
        #result {
            font-family: monospace;
            white-space: pre;
            border: 1px solid #ccc;
            padding: 10px;
            height: 300px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <h1>Browser CPU Load Test</h1>
    <div id="status">Running continuous calculations...</div>
    <div id="result"></div>

    <script>
        const resultDiv = document.getElementById('result');
        const statusDiv = document.getElementById('status');
        
        function runMatrixOperations() {
            const size = 300;
            const matrix1 = [];
            const matrix2 = [];
            
            for (let i = 0; i < size; i++) {
                matrix1[i] = [];
                matrix2[i] = [];
                for (let j = 0; j < size; j++) {
                    matrix1[i][j] = Math.random();
                    matrix2[i][j] = Math.random();
                }
            }
            
            const result = [];
            for (let i = 0; i < size; i++) {
                result[i] = [];
                for (let j = 0; j < size; j++) {
                    result[i][j] = 0;
                    for (let k = 0; k < size; k++) {
                        result[i][j] += matrix1[i][k] * matrix2[k][j];
                    }
                }
            }
            
            return result;
        }
        
        function calculatePrimes(max) {
            const primes = [];
            for (let i = 2; i <= max; i++) {
                let isPrime = true;
                for (let j = 2; j <= Math.sqrt(i); j++) {
                    if (i % j === 0) {
                        isPrime = false;
                        break;
                    }
                }
                if (isPrime) {
                    primes.push(i);
                }
            }
            return primes;
        }

        let iterationCount = 0;
        function runContinuousCalculations() {
            iterationCount++;
            
            if (iterationCount % 5 === 0) {
                const primes = calculatePrimes(10000);
                resultDiv.textContent = `Iteration ${iterationCount}\\nFound ${primes.length} prime numbers up to 10000\\n`;
            } else {
                const startTime = performance.now();
                runMatrixOperations();
                const endTime = performance.now();
                
                resultDiv.textContent = `Iteration ${iterationCount}\\nMatrix operation completed in ${(endTime - startTime).toFixed(2)} ms\\n`;
            }
            
            statusDiv.textContent = `Running continuous calculations... (Iteration: ${iterationCount})`;
            
            setTimeout(runContinuousCalculations, 100);
        }
        
        runContinuousCalculations();
    </script>
</body>
</html>
"""

def get_video_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Browser Power Test - Video</title>
        <style>
            body { margin: 0; padding: 0; background-color: black; }
            video { width: 100%; height: 100vh; }
        </style>
        <script>
            window.onload = function() {
                var video = document.querySelector('video');
                
                var playPromise = video.play();
                
                if (playPromise !== undefined) {
                    playPromise.then(_ => {
                        console.log('Autoplay started successfully');
                    })
                    .catch(error => {
                        console.log('Autoplay failed: ' + error);
                        document.addEventListener('click', function() {
                            video.play();
                        }, { once: true });
                    });
                }
                
                video.addEventListener('pause', function() {
                    video.play();
                });
                
                video.addEventListener('ended', function() {
                    video.currentTime = 0;
                    video.play();
                });
            }
        </script>
    </head>
    <body>
        <video muted autoplay loop playsinline>
            <!-- Video sources will be added dynamically -->
        </video>
    </body>
    </html>
    """