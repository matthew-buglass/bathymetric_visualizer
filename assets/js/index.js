import * as THREE from 'three';
import { ArcballControls } from 'three/addons/controls/ArcballControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const width = parent.innerWidth * 0.78;
const height = parent.innerHeight * 0.9;

// init
let camera;
let scene;
let axesHelper;
let renderer;
let controls;
let directionalLight;

// Add a water level reference
let waterGeometry;
let waterMaterial;
let waterMesh;

// Materials
let mesh_material;
let vertex_material;
let num_initial_children;

let benchy;
let benchyX;
let benchyY;

export async function init() {
	// Camera
	camera = new THREE.PerspectiveCamera( 50, width / height, 0.01, 1000 );
	camera.lookAt(0, 0, 0);
	camera.position.set(10, 10, 10);
	camera.updateProjectionMatrix();

	// Scene
	scene = new THREE.Scene();
	scene.background = new THREE.Color( 0xcccccc );

	// Axes helper
	axesHelper = new THREE.AxesHelper( 5 );
	scene.add( axesHelper );

	// Renderer
	renderer = new THREE.WebGLRenderer( { antialias: true } );
	renderer.setSize( width, height );

	// Controls
	controls = new ArcballControls( camera, renderer.domElement, scene );
	const initialControlState = '{"arcballState":{"cameraFar":1000,"cameraFov":50,"cameraMatrix":{"elements":[-0.9681388942741919,0.25023993639737485,-0.009330360410478357,0,-0.08440571738177859,-0.2910196978208815,0.9529864691345388,0,0.23575995475656714,0.9234108022500503,0.3028691698095068,0,8.067438461652268,31.741413566846084,11.588700413903558,1]},"cameraNear":0.01,"cameraUp":{"x":-0.0844057173817784,"y":-0.2910196978208807,"z":0.9529864691345364},"cameraZoom":1,"gizmoMatrix":{"elements":[2.0199645277949543,0,0,0,0,2.0199645277949543,0,0,0,0,2.0199645277949543,0,-0.18105073280580197,-0.5657864929351921,0.9922737345392729,1]}}}';
	controls.addEventListener( 'change', function () {
		renderer.render( scene, camera );
	});
	controls.setStateFromJSON(initialControlState);
	controls.update();

	// Lighting
	directionalLight = new THREE.DirectionalLight( 0x404040, 10 );
	directionalLight.position.set(  1, 1, 1 ).normalize();
	directionalLight.lookAt(0, 0, 0)
	scene.add( directionalLight );

	// Water
	waterGeometry = new THREE.PlaneGeometry(10000, 10000);
	waterMaterial = new THREE.MeshBasicMaterial( { color: 0x87ceeb, transparent: true } );
	waterMesh = new THREE.Mesh(waterGeometry, waterMaterial);
	scene.add( waterMesh );

	// Mesh and vertex materials
	mesh_material = new THREE.MeshMatcapMaterial( { color: 0xcd7f32, transparent: true } );
	vertex_material = new THREE.MeshBasicMaterial( { color: 0x000000, transparent: true } );
	setVertexOpacity(0);

	// Benchy
	benchyX = 0;
	benchyY = 0;
	await load_benchy()

	// Final setup
	num_initial_children = 4;
	document.getElementById("render-region").appendChild( renderer.domElement );
	window.addEventListener( 'resize', onWindowResize );

	animate();
}

export async function load_benchy() {
	const loader = new GLTFLoader()
	loader.load(
		'/static/models/9m_benchy.gltf',
		function ( gltf ) {
			console.log('Benchy loaded')
			benchy = gltf.scene;
			scene.add( benchy );
			moveBenchyTo( benchyX, benchyY );
			console.log('Benchy rendered');
		},
		(xhr) => {
			console.log('Loading Bench')
		},
		(error) => {
			console.log(error)
		}
	)
}

export function addData( vertices, face_indices ) {
	const geometry = new THREE.BufferGeometry();
	geometry.computeVertexNormals()
	geometry.setAttribute( 'position', new THREE.BufferAttribute( new Float32Array(vertices), 3 )  );
	geometry.setIndex( face_indices );
	geometry.computeVertexNormals();

	const mesh = new THREE.Mesh( geometry, mesh_material );
	// set the mesh to be drawn last so it is above the transparent vertices
	mesh.renderOrder = -1
	// Clear the scene of all but the initial children
	clearMesh();
	scene.add( mesh );

	// // update Benchy's position
	if (vertices.length > 2) {
		moveBenchyTo(vertices.length - 3, vertices.length - 2)
	}

	render()
}

function clearMesh() {
	while(scene.children.length > num_initial_children){
		scene.remove(scene.children[num_initial_children]);
	}
}

export function addVertexMarkers( vertices ) {
	// Vertices is a flat list of coordinates in the order [x1, y1, z1, x2, y2, z2, ...]
	for (let i = 0; i < vertices.length; i += 3) {
		const x = vertices[i];
		const y = vertices[i + 1];
		const z = vertices[i + 2];

		const sphereGeometry = new THREE.SphereGeometry(0.25, 6, 4);
		sphereGeometry.computeVertexNormals();
		sphereGeometry.translate(x, y, z)
		const vertex = new THREE.Mesh( sphereGeometry, vertex_material );
		scene.add( vertex );

	}
}

export function removeVertexMarkers() {
	while(scene.children.length > num_initial_children + 1){
		scene.remove(scene.children[num_initial_children + 1]);
	}
}

export function setMeshOpacity( value ) {
	mesh_material.opacity = value;
	render();
}

export function setVertexOpacity( value ) {
	vertex_material.opacity = value;
	render();
}

export function setWaterOpacity( value ) {
	waterMaterial.opacity = value;
	render();
}

function moveBenchyTo( x, y ) {
	benchyX = x;
	benchyY = y;
	if (typeof benchy !== "undefined") {
		benchy.position.x = benchyX;
		benchy.position.y = benchyY;
		scene.add(benchy);
	}
}

function onWindowResize() {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();

	controls.handleResize();

	renderer.setSize( window.innerWidth, window.innerHeight );
}

function animate() {
	requestAnimationFrame( animate );
	controls.update(); // only required if controls.enableDamping = true, or if controls.autoRotate = true
	render();
}

function render() {
	renderer.render( scene, camera );
}
