<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

// Get parameters from request
$url = isset($_GET['url']) ? $_GET['url'] : 'http://localhost:8000';
$maxwidth = isset($_GET['maxwidth']) ? intval($_GET['maxwidth']) : 800;
$maxheight = isset($_GET['maxheight']) ? intval($_GET['maxheight']) : 600;
$format = isset($_GET['format']) ? $_GET['format'] : 'json';

// Calculate responsive dimensions
$width = min($maxwidth, 800);
$height = min($maxheight, 600);

// Create oEmbed response
$response = array(
    'version' => '1.0',
    'type' => 'rich',
    'title' => 'La Garita Fire District Map',
    'author_name' => 'La Garita Fire District',
    'provider_name' => 'La Garita Fire District Mapping',
    'provider_url' => parse_url($url, PHP_URL_SCHEME) . '://' . parse_url($url, PHP_URL_HOST),
    'cache_age' => 3600,
    'html' => '<iframe src="' . htmlspecialchars($url) . '" width="' . $width . '" height="' . $height . '" frameborder="0" allowfullscreen="true" style="max-width: 100%; border: 1px solid #ccc; border-radius: 4px;"></iframe>',
    'width' => $width,
    'height' => $height,
    'thumbnail_url' => 'https://tile.openstreetmap.org/9/107/193.png',
    'thumbnail_width' => 256,
    'thumbnail_height' => 256
);

// Output based on format
if ($format === 'xml') {
    header('Content-Type: text/xml');
    echo '<?xml version="1.0" encoding="utf-8"?>';
    echo '<oembed>';
    foreach ($response as $key => $value) {
        echo '<' . $key . '>' . htmlspecialchars($value) . '</' . $key . '>';
    }
    echo '</oembed>';
} else {
    echo json_encode($response, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
}
?>