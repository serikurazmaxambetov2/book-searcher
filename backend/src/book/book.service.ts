import { Injectable } from '@nestjs/common';
import { PrismaService } from 'src/prisma/prisma.service';
import { BookCreateDto } from './dto/book-create.dto';

@Injectable()
export class BookService {
  constructor(private prisma: PrismaService) {}

  async create(dto: BookCreateDto) {
    return await this.prisma.book.create({ data: dto });
  }

  async findOneById(id: number) {
    return await this.prisma.book.findFirst({ where: { id } });
  }
}
