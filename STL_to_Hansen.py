import sys
import numpy
from stl import mesh

class HanMesh:
  def __init__(self):
    self.element_counter = 0
    self.vertexs = []
    self.edges = []
    self.faces = []

  def addFace(self, vectors):
    self.vertexs.append(vectors[0])
    self.vertexs.append(vectors[1])
    self.vertexs.append(vectors[2])

    self.edges.append([self.element_counter + 0, self.element_counter + 1])
    self.edges.append([self.element_counter + 1, self.element_counter + 2])
    self.edges.append([self.element_counter + 2, self.element_counter + 0])

    self.faces.append([self.element_counter + 0, self.element_counter + 1, self.element_counter + 2])

    self.element_counter += 3

  def print(self):
    print(self.faces)



if(len(sys.argv) < 2):
  print('Pass stl files into the program and output *.h and *.cpp files in Hansen\'s format')

for path in sys.argv[1:]:
  filename = (path.split(".")[0])
  out_h   = open(filename + ".h", "w")
  out_cpp = open(filename + ".cpp", "w")

  mesh = mesh.Mesh.from_file(path)
  mmesh = HanMesh()

  for face in mesh.vectors:
    mmesh.addFace(face)

  out_h.write('#ifndef CS250_{0}_H\n'.format(filename))
  out_h.write('#define CS250_{0}_H\n\n'.format(filename))
  out_h.write('#include "Mesh.h"\n\n')
  out_h.write('class {0} : public Mesh\n'.format(filename))
  out_h.write('{\n')
  out_h.write('public:\n')
  out_h.write('  int VertexCount();\n')
  out_h.write('  Point GetVertex(int i);\n')
  out_h.write('  Vector Dimensions(void);\n')
  out_h.write('  Point Center(void);\n')
  out_h.write('  int FaceCount(void);\n')
  out_h.write('  Face GetFace(int i);\n')
  out_h.write('  int EdgeCount(void);\n')
  out_h.write('  Edge GetEdge(int i);\n')
  out_h.write('private:\n')
  out_h.write('  static const Point vertices[{0}];\n'.format(len(mmesh.vertexs)))
  out_h.write('  static const Face faces[{0}];\n'.format(len(mmesh.faces)))
  out_h.write('  static const Edge edges[{0}];\n'.format(len(mmesh.edges)))
  out_h.write('};\n\n')
  out_h.write('#endif')
  out_h.close()

  out_cpp.write('#include "{0}.h"\n\n'.format(filename))
  
  out_cpp.write('const Point {0}::vertices[{1}] = \n'.format(filename, len(mmesh.vertexs)))
  out_cpp.write('{\n')
  formatList = []
  for vert in mmesh.vertexs:
    formatList.append('  Point(%.5ff, %.5ff, %.5ff)' % (vert[0], vert[1], vert[2]))
  out_cpp.write(',\n'.join(formatList))
  out_cpp.write('\n};\n\n')

  out_cpp.write('const Mesh::Face {0}::faces[{1}] = \n'.format(filename, len(mmesh.faces)))
  out_cpp.write('{\n')
  formatList = []
  for face in mmesh.faces:
    formatList.append('  Mesh::Face({0}, {1}, {2})'.format(face[0], face[1], face[2]))
  out_cpp.write(',\n'.join(formatList))
  out_cpp.write('\n};\n\n')

  out_cpp.write('const Mesh::Edge {0}::edges[{1}] = \n'.format(filename, len(mmesh.edges)))
  out_cpp.write('{\n')
  formatList = []
  for edge in mmesh.edges:
    formatList.append('  Mesh::Edge({0}, {1})'.format(edge[0], edge[1]))
  out_cpp.write(',\n'.join(formatList))
  out_cpp.write('\n};\n\n')


  out_cpp.write('int {0}::VertexCount()\n'.format(filename))
  out_cpp.write('{\n')
  out_cpp.write('  return {0};\n'.format(len(mmesh.vertexs)))
  out_cpp.write('}\n\n')

  out_cpp.write('Point  {0}::GetVertex(int i)\n'.format(filename))
  out_cpp.write('{\n')
  out_cpp.write('  return vertices[i];\n')
  out_cpp.write('}\n\n')

  out_cpp.write('Vector {0}::Dimensions()\n'.format(filename))
  out_cpp.write('{\n')
  out_cpp.write('  return Vector(2, 2, 2);\n')
  out_cpp.write('}\n\n')

  out_cpp.write('Point {0}::Center()\n'.format(filename))
  out_cpp.write('{\n')
  out_cpp.write('  return Point(0, 0, 0);\n')
  out_cpp.write('}\n\n')

  out_cpp.write('int {0}::FaceCount()\n'.format(filename))
  out_cpp.write('{\n')
  out_cpp.write('  return {0};\n'.format(len(mmesh.faces)))
  out_cpp.write('}\n\n')

  out_cpp.write('Mesh::Face {0}::GetFace(int i)\n'.format(filename))
  out_cpp.write('{\n')
  out_cpp.write('  return faces[i];\n')
  out_cpp.write('}\n\n')

  out_cpp.write('int {0}::EdgeCount()\n'.format(filename))
  out_cpp.write('{\n')
  out_cpp.write('  return {0};\n'.format(len(mmesh.edges)))
  out_cpp.write('}\n\n')

  out_cpp.write('Mesh::Edge {0}::GetEdge(int i)\n'.format(filename))
  out_cpp.write('{\n')
  out_cpp.write('  return edges[i];\n')
  out_cpp.write('}\n')

  out_cpp.close()


