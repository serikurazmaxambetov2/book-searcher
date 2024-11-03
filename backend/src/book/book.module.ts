import { Module } from '@nestjs/common';
import { BookService } from './book.service';
import { BookController } from './book.controller';
import { PrismaModule } from 'src/prisma/prisma.module';
import { SearchModule } from 'src/search/search.module';

@Module({
  imports: [PrismaModule, SearchModule],
  controllers: [BookController],
  providers: [BookService],
})
export class BookModule {}
